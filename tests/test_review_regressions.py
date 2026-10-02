"""Second-pass review controls. Synthetic data; no ERP or credentials are used."""
import copy
import io
import os
import struct
import sys
import tempfile
import unittest
import zlib
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import tirqa_core as core
import tirqa_runner as runner
import package_skill
from test_tirqa import case, profile, policy


from qa_test_fixtures import png_bytes


def complete_result():
    c, p = case(), profile()
    return {"schema_version": 1, "exit_code": 0, "private_cleanup": "REMOVED", "evidence_status": "LOCAL_ONLY", "run_id": "review-control", "case_id": c["case_id"],
            "status": "PASS", "counts": {"tests": 1, "failures": 0, "errors": 0, "skipped": 0},
            "checks_expected": 1, "checks_passed": 1, "cleanup": "SESSION_CLOSED", "screenshots": 1,
            "identity": [{"kind": k, "observed": True} for k in ["environment", "group", "branch", "routine"]],
            "observations": [{"step": 1, "method": "GetValue", "source_id": "S1", "status": "PASS",
                              "expected": "000001 ", "observed": "000001 "}],
            "bundle_sha256": core.bundle_manifest(core.bundle_files(c, p))["bundle_sha256"],
            "erp_validated": False, "execution_mode": "simulated"}


class EvidenceReviewTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        core.write_json(self.root / "case.json", case())
        core.write_json(self.root / "profile.json", profile())
        (self.root / "screenshots").mkdir()

    def result(self, data=None, image=True):
        core.write_json(self.root / "result.json", data or complete_result())
        if image: (self.root / "screenshots" / "end.png").write_bytes(png_bytes())

    def test_pass_without_actual_image_is_blocked(self):
        self.result(image=False)
        with self.assertRaises(core.Blocked): runner.collect(self.root, create=True)

    def test_summary_named_extra_file_is_not_ignored(self):
        data = complete_result(); data["status"] = "ERROR"
        self.result(data); runner.collect(self.root, create=True)
        (self.root / "nested").mkdir()
        (self.root / "nested" / "summary.md").write_text("untracked")
        with self.assertRaises(core.Blocked): runner.collect(self.root)

    def test_boolean_counter_is_not_integer(self):
        data = complete_result(); data["counts"]["tests"] = True
        self.result(data)
        with self.assertRaises(core.Blocked): runner.collect(self.root, create=True)

    def test_missing_observation_is_not_pass(self):
        data = complete_result(); data["observations"] = []
        self.result(data)
        with self.assertRaises(core.Blocked): runner.collect(self.root, create=True)

    def test_changed_observed_value_is_not_pass(self):
        data = complete_result(); data["observations"][0]["observed"] = "other"
        self.result(data)
        with self.assertRaises(core.Blocked): runner.collect(self.root, create=True)

    def test_fake_png_is_not_evidence(self):
        self.result(); (self.root / "screenshots" / "end.png").write_bytes(b"NOT_A_PNG")
        with self.assertRaises(core.Blocked): runner.collect(self.root, create=True)

    def test_truncated_png_is_not_evidence(self):
        self.result(); (self.root / "screenshots" / "end.png").write_bytes(png_bytes()[:-5])
        with self.assertRaises(core.Blocked): runner.collect(self.root, create=True)

    def test_case_hash_mismatch_is_blocked(self):
        data = complete_result(); data["bundle_sha256"] = "0" * 64
        self.result(data)
        with self.assertRaises(core.Blocked): runner.collect(self.root, create=True)

    def test_simulation_cannot_claim_erp_validation(self):
        data = complete_result(); data["erp_validated"] = True
        self.result(data)
        with self.assertRaises(core.Blocked): runner.collect(self.root, create=True)

    def test_valid_synthetic_evidence_is_accepted_as_simulated(self):
        self.result(); value = runner.collect(self.root, create=True)
        self.assertEqual(value["status"], "PASS"); self.assertFalse(value["erp_validated"])


class OperationalReviewTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name); self.bundle = self.root / "bundle"
        self.manifest = core.generate(case(), profile(), self.bundle)
        self.approval = self.root / "approval.json"
        self.approved = policy(self.manifest)
        core.write_json(self.approval, self.approved); self.approval.chmod(0o600)
        self.output = self.root / "run"

    def run_with(self, process, extra):
        with patch.object(runner, "preflight", return_value={"status": "READY_FOR_AUTHORIZATION"}), \
             patch.dict(os.environ, {"TIR_USER": "qa_user", "TIR_PASSWORD": "test_secret"}), \
             patch.object(runner, "private_directory", side_effect=lambda p: p.mkdir(parents=True)), \
             patch.object(runner.subprocess, "Popen", return_value=process), extra:
            return runner.execute(self.bundle, self.approval, self.output)

    def test_interruption_stops_owned_process(self):
        process = type("Fake", (), {"wait": lambda self, **kw: (_ for _ in ()).throw(KeyboardInterrupt()), "poll": lambda self: None})()
        with patch.object(runner, "stop_tree") as stop:
            try: result = self.run_with(process, patch.dict(os.environ, {}))
            except KeyboardInterrupt: result = {"status": "INTERRUPTED_WITHOUT_RESULT"}
            self.assertEqual(stop.call_count, 1)
            self.assertEqual(result["status"], "ERROR")

    def test_cleanup_failure_produces_error_record(self):
        process = type("Fake", (), {"wait": lambda self, **kw: 1, "poll": lambda self: 1})()
        try: result = self.run_with(process, patch.object(runner.shutil, "rmtree", side_effect=PermissionError("injected")))
        except PermissionError: result = {"status": "NO_ERROR_RECORD"}
        self.assertEqual(result["status"], "ERROR")
        self.assertTrue((self.output / "result.json").is_file())
        self.assertFalse((self.output / ".private" / "config.json").exists())

    def test_approval_hash_uses_approved_snapshot(self):
        approval = self.approval
        def wait(self, **kw):
            approval.write_text('{"modified":"while running"}')
            return 1
        process = type("Fake", (), {"wait": wait, "poll": lambda self: 1})()
        result = self.run_with(process, patch.dict(os.environ, {}))
        self.assertEqual(result["approval_sha256"], core.digest(core.encoded(self.approved)))

    def test_control_characters_in_url_are_blocked(self):
        p = profile(); p["config"]["Url"] = "https://erp.qa.test/\n"
        with self.assertRaises(core.Blocked): core.validate_profile(p)

    def test_package_identical_for_lf_and_crlf_worktrees(self):
        a, b = self.root / "lf", self.root / "crlf"
        a.mkdir(); b.mkdir()
        for root, nl in [(a, b"\n"), (b, b"\r\n")]:
            (root / "VERSION").write_bytes(b"0.2.0-rc.3" + nl)
            (root / "README.md").write_bytes(b"# Fixture" + nl + b"No ERP" + nl)
        with patch("sys.stdout", new_callable=io.StringIO):
            one = package_skill.build_zip(a).read_bytes(); two = package_skill.build_zip(b).read_bytes()
        self.assertEqual(one, two)


if __name__ == "__main__": unittest.main()
