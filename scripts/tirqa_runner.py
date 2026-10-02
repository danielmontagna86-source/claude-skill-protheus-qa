"""Isolated, read-only TIR pilot runner. Never import TIR during static commands."""
from __future__ import annotations

import csv
import io
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import unittest
import uuid
from datetime import datetime, timezone
from pathlib import Path

# Support an isolated (-I) worker without consulting cwd or PYTHONPATH.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from tirqa_core import (ASSERTIONS, CONTRACT, Blocked, TIR_VERSION, approve,
                        bundle_files, digest, encoded, engine_hash, load_json,
                        preflight, require, validate_profile, verify_bundle, write_json)


def utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def private_directory(path: Path) -> None:
    require(not path.exists(), "output_exists")
    require(not str(path).startswith("\\\\"), "network_share_not_allowed")
    path.mkdir(parents=True, mode=0o700)
    if os.name == "nt":
        output = subprocess.run(["whoami", "/user", "/fo", "csv", "/nh"],
                                check=True, capture_output=True, text=True).stdout
        sid = next(csv.reader(io.StringIO(output)))[1]
        require(re.fullmatch(r"S-\d+(?:-\d+)+", sid) is not None, "windows_sid_unavailable")
        subprocess.run(["icacls", str(path), "/inheritance:r", "/grant:r",
                        f"*{sid}:(OI)(CI)F"], check=True, capture_output=True)
    else:
        path.chmod(0o700)


def scrub(value: object, secrets: tuple[str, ...]) -> object:
    if isinstance(value, str):
        for secret in sorted((s for s in secrets if s), key=len, reverse=True):
            value = value.replace(secret, "[REDACTED]")
        return value
    if isinstance(value, list):
        return [scrub(v, secrets) for v in value]
    if isinstance(value, dict):
        return {k: scrub(v, secrets) for k, v in value.items()}
    return value


class CaseTest(unittest.TestCase):
    """One case/session/process; configuration is injected only by the approved worker."""
    case: dict = {}
    profile: dict = {}
    runtime: dict | None = None
    helper_factory = None

    def setUp(self) -> None:
        require(self.runtime is not None, "approved_runner_required")
        self.observations = []
        self.identity = []
        self.business_checks = 0
        self.cleanup_status = "NOT_STARTED"
        self.screenshot_status = "NOT_STARTED"
        self.helper = type(self).helper_factory(self.runtime["config_path"])
        self.addCleanup(self._finish)
        self.helper.Start()
        self.helper.Setup(**self.profile["setup"])
        self.helper.AssertTrue()
        for item in self.profile["identity_checks"]:
            self._identity(item["kind"], item["text"])
        self.helper.Program(self.case["routine"])
        self._identity("routine", self.case["routine_marker"])

    def _identity(self, kind: str, marker: str) -> None:
        actual = self.helper.IfExists(marker, timeout=self.profile["config"]["TimeOut"])
        self.identity.append({"kind": kind, "expected": True, "observed": actual is True})
        self.assertIs(actual, True, f"identity_check_failed:{kind}")
        self.helper.AssertTrue()

    def _finish(self) -> None:
        try:
            self.helper.Screenshot(filename=self.case["case_id"] + "-end")
            self.screenshot_status = "CAPTURE_REQUESTED"
        finally:
            self.cleanup_status = "ERROR"
            self.helper.TearDown()
            self.cleanup_status = "SESSION_CLOSED"

    def test_case(self) -> None:
        for index, step in enumerate(self.case["steps"], start=1):
            method, kwargs = step["method"], step["kwargs"]
            event = {"step": index, "method": method, "source_id": step["source_id"],
                     "status": "ERROR"}
            self.observations.append(event)
            if method == "CheckResult":
                read_args = {k: v for k, v in kwargs.items() if k != "user_value"}
                actual = self.helper.GetValue(**read_args)
                event.update(expected=kwargs["user_value"], observed=actual)
                self.helper.CheckResult(**kwargs)  # CheckResult is NOT boolean.
                if kwargs.get("grid", False):
                    self.helper.LoadGrid()
                self.helper.AssertTrue()
                self._compare(actual, kwargs["user_value"], event)
            elif method in {"GetValue", "IfExists"}:
                actual = getattr(self.helper, method)(**kwargs)
                event.update(expected=step["expected"], observed=actual)
                self._compare(actual, step["expected"], event)
            else:
                getattr(self.helper, method)(**kwargs)
            self.helper.AssertTrue()  # Flush TIR's own accumulated error state.
            event["status"] = "PASS"

    def _compare(self, actual: object, expected: object, event: dict) -> None:
        event["status"] = "FAIL"
        self.assertIs(type(actual), type(expected), "observed_type_mismatch")
        self.assertEqual(actual, expected, "observed_value_mismatch")
        self.business_checks += 1


def run_worker(directory: Path, factory=None) -> int:
    case, profile, manifest = verify_bundle(directory / "bundle")
    validate_profile(profile, execution=True)
    runtime = load_json(directory / "runtime.json")
    require(runtime["engine_sha256"] == engine_hash(), "worker_engine_changed")
    require(runtime["bundle_sha256"] == manifest["bundle_sha256"], "worker_bundle_changed")
    simulated = factory is not None
    if factory is None:
        require(preflight(profile)["status"] == "READY_FOR_AUTHORIZATION", "worker_preflight_failed")
        from tir import Webapp  # The ONLY TIR import; after all execution gates.
        factory = lambda config_path: Webapp(config_path=config_path, autostart=False)
    test_type = type("ApprovedCase", (CaseTest,),
                     {"case": case, "profile": profile, "runtime": runtime,
                      "helper_factory": staticmethod(factory)})
    test = test_type("test_case")
    started = utc()
    result = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0).run(unittest.TestSuite([test]))
    screenshots = [p for p in Path(runtime["screenshots"]).rglob("*")
                   if p.is_file() and not p.is_symlink() and p.suffix.lower() in {".png", ".jpg"}
                   and p.stat().st_size > 0]
    expected_checks = sum(s["method"] in ASSERTIONS for s in case["steps"])
    checks = getattr(test, "business_checks", 0)
    cleanup = getattr(test, "cleanup_status", "NOT_STARTED")
    identity = getattr(test, "identity", [])
    counts = {"tests": result.testsRun, "failures": len(result.failures),
              "errors": len(result.errors), "skipped": len(result.skipped)}
    complete = (counts == {"tests": 1, "failures": 0, "errors": 0, "skipped": 0}
                and checks == expected_checks and expected_checks > 0 and bool(screenshots)
                and cleanup == "SESSION_CLOSED" and len(identity) == 4
                and all(i["observed"] is True for i in identity))
    status = "PASS" if complete else ("ERROR" if result.errors else "FAIL")
    if result.wasSuccessful() and not complete:
        status = "ERROR"  # Missing evidence is not success.
    payload = {"schema_version": 1, "case_id": case["case_id"], "status": status,
               "counts": counts, "checks_expected": expected_checks, "checks_passed": checks,
               "identity": identity, "observations": getattr(test, "observations", []),
               "cleanup": cleanup, "screenshots": len(screenshots), "started_at": started,
               "finished_at": utc(), "erp_validated": complete and not simulated,
               "execution_mode": "simulated" if simulated else "live",
               "test_engine": "unittest", "tir_version": TIR_VERSION}
    # Raw unittest tracebacks may contain credentials. Keep only deterministic status here.
    write_json(directory / "worker-result.json", payload)
    return 0 if status == "PASS" else 1


def stop_tree(process: subprocess.Popen) -> None:
    if os.name == "nt":
        subprocess.run(["taskkill", "/PID", str(process.pid), "/T", "/F"],
                       capture_output=True, check=False)
    else:
        try:
            os.killpg(process.pid, signal.SIGTERM)
            process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    try:
        process.wait(timeout=10)
    except subprocess.TimeoutExpired:
        raise Blocked("owned_process_tree_not_stopped") from None


def execute(bundle: Path, policy_path: Path, output: Path) -> dict:
    case, profile, manifest = verify_bundle(bundle)
    require(not output.is_symlink(), "symlink_output")
    output = output.resolve()
    validate_profile(profile, execution=True)
    root = Path(__file__).resolve().parents[1]
    require(not output.resolve().is_relative_to(root), "evidence_must_be_outside_skill")
    require(not policy_path.resolve().is_relative_to(root)
            and not policy_path.resolve().is_relative_to(bundle.resolve()), "external_policy_required")
    if os.name != "nt":
        require(policy_path.stat().st_mode & 0o022 == 0, "policy_must_not_be_group_world_writable")
    policy = load_json(policy_path)
    approve(policy, case, profile, manifest)
    require(preflight(profile)["status"] == "READY_FOR_AUTHORIZATION", "runtime_not_ready")
    username, password = os.environ.get("TIR_USER", ""), os.environ.get("TIR_PASSWORD", "")
    require(bool(username) and bool(password), "credentials_missing")
    secrets = (username, password)
    private_directory(output)
    private = output / ".private"
    private_directory(private)
    snapshots = private / "bundle"
    snapshots.mkdir()
    for name, content in bundle_files(case, profile).items():
        (snapshots / name).write_bytes(content)
    write_json(snapshots / "manifest.json", manifest)
    engine = private / "engine"
    engine.mkdir()
    source_dir = Path(__file__).resolve().parent
    for name in ("tirqa_core.py", "tirqa_runner.py"):
        (engine / name).write_bytes((source_dir / name).read_bytes())
    snapshot_hash = digest(encoded({n: digest((engine / n).read_bytes())
                                   for n in ("tirqa_core.py", "tirqa_runner.py")}))
    require(snapshot_hash == policy["engine_sha256"], "engine_changed_during_snapshot")
    (output / "screenshots").mkdir()
    (output / "logs").mkdir()
    config = dict(profile["config"])
    config.update(User=username, Password=password, ScreenShot=True, NewLog=False,
                  LogInfoConfig=False, DebugLog=False, LogFile=True,
                  LogFolder=str((output / "logs").resolve()),
                  ScreenshotFolder=str((output / "screenshots").resolve()),
                  ChromeDriverAutoInstall=False)
    run_id = uuid.uuid4().hex
    payload = {"schema_version": 1, "case_id": case["case_id"], "status": "ERROR",
               "erp_validated": False, "reason": "worker_did_not_complete"}
    process = None
    started = utc()
    try:
        write_json(private / "config.json", config)
        write_json(private / "runtime.json", {"config_path": str((private / "config.json").resolve()),
                   "screenshots": str((output / "screenshots").resolve()),
                   "bundle_sha256": manifest["bundle_sha256"], "engine_sha256": snapshot_hash})
        keep = {"PATH", "SYSTEMROOT", "WINDIR", "USERPROFILE", "APPDATA", "LOCALAPPDATA",
                "TEMP", "TMP", "HOME", "LANG", "DISPLAY", "XAUTHORITY",
                "SSL_CERT_FILE", "SSL_CERT_DIR", "REQUESTS_CA_BUNDLE"}
        env = {k: v for k, v in os.environ.items() if k.upper() in keep}
        options = ({"creationflags": subprocess.CREATE_NEW_PROCESS_GROUP} if os.name == "nt"
                   else {"start_new_session": True})
        with (private / "console.raw").open("wb") as console:
            process = subprocess.Popen([sys.executable, "-I", str(engine / "tirqa_runner.py"),
                                        "--worker", str(private.resolve())],
                                       cwd=private, env=env, stdout=console,
                                       stderr=subprocess.STDOUT, **options)
            try:
                code = process.wait(timeout=policy["max_seconds"])
            except subprocess.TimeoutExpired:
                stop_tree(process)
                code = 124
                payload["reason"] = "timeout_environment_state_requires_review"
        if (private / "worker-result.json").is_file():
            payload = load_json(private / "worker-result.json")
        if code != 0:
            payload["erp_validated"] = False
            if payload.get("status") == "PASS":
                payload.update(status="ERROR", reason="worker_exit_inconsistent")
        require(code != 0 or payload.get("status") == "PASS", "worker_success_without_evidence")
        payload["exit_code"] = code
    except Exception as exc:
        if process is not None and process.poll() is None:
            stop_tree(process)
        payload.update(status="ERROR", erp_validated=False, reason=type(exc).__name__)
    finally:
        # Console is quarantined, size-limited and redacted before it becomes an artifact.
        raw = private / "console.raw"
        if raw.exists() and raw.stat().st_size <= 20_000_000:
            content = scrub(raw.read_text(encoding="utf-8", errors="replace"), secrets)
            (output / "console.txt").write_text(content, encoding="utf-8")
        # Delete only the private directory created by this run; not the user's workspace.
        shutil.rmtree(private)
    payload.update(run_id=run_id, approved_by=policy["approved_by"],
                   approval_sha256=digest(policy_path.read_bytes()),
                   bundle_sha256=manifest["bundle_sha256"], engine_sha256=snapshot_hash,
                   started_at=started, finished_at=utc(),
                   homologation_scope="read_only_pilot_not_product_certification")
    write_json(output / "result.json", scrub(payload, secrets))
    write_json(output / "case.json", case)
    write_json(output / "profile.json", profile)
    # TIR logs/screenshots remain restricted local evidence, never uploaded automatically.
    collect(output, create=True)
    return payload


def artifacts(root: Path) -> dict:
    files = {}
    for path in sorted(root.rglob("*")):
        require(not path.is_symlink(), "symlink_in_evidence")
        if path.is_file() and path.name not in {"evidence-manifest.json", "summary.md"}:
            require(".private" not in path.relative_to(root).parts, "private_files_in_evidence")
            files[path.relative_to(root).as_posix()] = digest(path.read_bytes())
    return files


def collect(root: Path, create: bool = False) -> dict:
    require(not root.is_symlink(), "symlink_evidence_root")
    result = load_json(root / "result.json")
    require(result.get("status") in {"PASS", "FAIL", "ERROR", "BLOCKED", "NOT_RUN", "SKIPPED"},
            "invalid_result_status")
    if result["status"] == "PASS":
        counts = result.get("counts", {})
        expected = result.get("checks_expected", 0)
        require(counts == {"tests": 1, "failures": 0, "errors": 0, "skipped": 0}
                and type(expected) is int and expected > 0
                and result.get("checks_passed") == expected
                and result.get("cleanup") == "SESSION_CLOSED"
                and result.get("screenshots", 0) > 0, "invalid_pass_evidence")
        identity = result.get("identity", [])
        require(len(identity) == 4 and all(x.get("observed") is True for x in identity)
                and {x.get("kind") for x in identity} == {"environment", "group", "branch", "routine"},
                "invalid_pass_identity")
    found = artifacts(root)
    require("result.json" in found, "result_missing")
    manifest = {"schema_version": 1, "run_id": result["run_id"], "files": found}
    if create:
        write_json(root / "evidence-manifest.json", manifest)
    else:
        require(load_json(root / "evidence-manifest.json") == manifest, "evidence_integrity_failed")
    return {"status": result["status"], "run_id": result["run_id"], "integrity": "VERIFIED",
            "artifact_count": len(found), "authenticity": "not_cryptographically_signed",
            "uploaded": False, "erp_validated": result.get("erp_validated", False),
            "execution_mode": result.get("execution_mode", "not_recorded")}


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] != "--worker":
        raise SystemExit("Use run_tir_suite.py. This module is an internal isolated worker.")
    try:
        raise SystemExit(run_worker(Path(sys.argv[2])))
    except (Blocked, OSError, ValueError, KeyError, TypeError) as exc:
        print(type(exc).__name__, file=sys.stderr)
        raise SystemExit(2) from None
