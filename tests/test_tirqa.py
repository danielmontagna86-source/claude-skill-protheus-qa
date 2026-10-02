"""Deterministic offline controls; none of these tests connect to an ERP."""
from __future__ import annotations

import ast
import contextlib
import copy
import importlib.metadata
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import tirqa_core as core
import tirqa_runner as runner
from tirqa_cli import main


def profile():
    return {"schema_version": 1, "enabled": True, "environment_kind": "homologation",
            "tir_version": "2.14.10", "config": {"Url": "https://erp.qa.test/webapp/",
            "Environment": "QA", "Browser": "Chrome", "Language": "pt-br", "TimeOut": 10},
            "setup": {"initial_program": "SIGAFAT", "date": "01/10/2026", "group": "T1",
                      "branch": "01 ", "module": "05"},
            "identity_checks": [{"kind": "environment", "text": "QA environment"},
                                {"kind": "group", "text": "Test group"},
                                {"kind": "branch", "text": "Test branch"}],
            "baseline": {k: "synthetic unit-test fixture" for k in
                         ["release", "appserver", "webapp", "lib", "rpo", "interface_evidence"]}}


def case():
    return {"schema_version": 1, "case_id": "QA-001", "title": "Offline control",
            "routine": "U_QADEMO", "routine_marker": "Synthetic routine", "mode": "read_only",
            "sources": [{"id": "S1", "uri": "fixture:test_tirqa.py", "revision": "1", "status": "confirmed"}],
            "oracle": {"source_id": "S1", "description": "Independent synthetic constant", "approved_by": "Test fixture"},
            "fixture": {"synthetic": True, "description": "Not an actual Protheus record", "record_key": "000001 "},
            "steps": [{"method": "GetValue", "kwargs": {"field": "SYNTHETIC_CODE"},
                       "expected": "000001 ", "source_id": "S1"}]}


def policy(manifest, p=None):
    p = p or profile()
    return {"schema_version": 1, "environment_kind": "homologation",
            "target": {"Url": p["config"]["Url"], "Environment": "QA", "group": "T1", "branch": "01 "},
            "approved_by": "Offline test fixture, not a real operator",
            "expires_at": (datetime.now(timezone.utc) + timedelta(minutes=10)).isoformat(),
            "bundle_sha256": manifest["bundle_sha256"], "engine_sha256": core.engine_hash(),
            "allowed_buttons": ["Visualizar"], "integrations_blocked": True,
            "least_privilege_confirmed": True, "max_seconds": 30}


class FakeHelper:
    def __init__(self, screenshot_dir, value="000001 ", identity=True, image=True,
                 teardown_error=False, native_error=False):
        self.screenshot_dir, self.value = screenshot_dir, value
        self.identity, self.image = identity, image
        self.teardown_error, self.native_error = teardown_error, native_error
        self.calls = []

    def Start(self): self.calls.append("Start")
    def Setup(self, **kwargs): self.calls.append(("Setup", kwargs))
    def Program(self, program): self.calls.append(("Program", program))
    def IfExists(self, *args, **kwargs): return self.identity
    def GetValue(self, **kwargs): return self.value
    def CheckResult(self, **kwargs): self.calls.append("CheckResult")
    def LoadGrid(self): self.calls.append("LoadGrid")
    def AssertTrue(self):
        self.calls.append("AssertTrue")
        if self.native_error:
            raise AssertionError("native TIR failure")
    def Screenshot(self, filename):
        self.calls.append("Screenshot")
        if self.image:
            (self.screenshot_dir / (filename + ".png")).write_bytes(b"SYNTHETIC_IMAGE_NOT_ERP")
    def TearDown(self):
        self.calls.append("TearDown")
        if self.teardown_error:
            raise RuntimeError("teardown failed")


class ContractTests(unittest.TestCase):
    def test_valid_profile_and_case(self):
        core.validate_profile(profile()); core.validate_case(case())

    def test_block_profile_variants(self):
        variants = [dict(environment_kind="production"), dict(tir_version="latest"),
                    dict(enabled="false"), dict(schema_version=True), dict(extra="value")]
        for update in variants:
            with self.subTest(update=update), self.assertRaises(core.Blocked):
                p = profile(); p.update(update); core.validate_profile(p)

    def test_disabled_profile_not_executed(self):
        p = profile(); p["enabled"] = False
        core.validate_profile(p)
        with self.assertRaises(core.Blocked): core.validate_profile(p, execution=True)

    def test_invalid_config(self):
        variants = [{"Url": "http://erp.qa.test"}, {"Url": "https://user:pass@erp.qa.test"},
                    {"Url": "https://erp.example.invalid"}, {"Url": "https://erp.qa.test/?secret=x"},
                    {"Password": "never-commit-this"}, {"NewLog": True},
                    {"POUILogin": "False"}, {"TimeOut": True}, {"TimeOut": 999}]
        for update in variants:
            with self.subTest(update=update), self.assertRaises(core.Blocked):
                p = profile(); p["config"].update(update); core.validate_profile(p)

    def test_missing_identity_scope(self):
        p = profile(); p["identity_checks"][2]["kind"] = "group"
        with self.assertRaises(core.Blocked): core.validate_profile(p)

    def test_date_checked(self):
        p = profile(); p["setup"]["date"] = "31/02/2026"
        with self.assertRaises(ValueError): core.validate_profile(p)

    def test_placeholder_blocked(self):
        p = profile(); p["baseline"]["rpo"] = "PREENCHER"
        with self.assertRaises(core.Blocked): core.validate_profile(p)

    def test_case_missing_and_unknown_keys(self):
        for key in case():
            with self.subTest(key=key), self.assertRaises(core.Blocked):
                c = case(); del c[key]; core.validate_case(c)
        c = case(); c["unknown"] = 1
        with self.assertRaises(core.Blocked): core.validate_case(c)

    def test_case_writes_blocked(self):
        c = case(); c["mode"] = "reversible_write"
        with self.assertRaisesRegex(core.Blocked, "writes_not_released"): core.validate_case(c)

    def test_non_synthetic_fixture_blocked(self):
        c = case(); c["fixture"]["synthetic"] = False
        with self.assertRaises(core.Blocked): core.validate_case(c)

    def test_unconfirmed_source_blocked(self):
        c = case(); c["sources"][0]["status"] = "hypothesis"
        with self.assertRaises(core.Blocked): core.validate_case(c)

    def test_duplicate_source_blocked(self):
        c = case(); c["sources"].append(dict(c["sources"][0]))
        with self.assertRaises(core.Blocked): core.validate_case(c)

    def test_missing_oracle_blocked(self):
        c = case(); c["oracle"]["approved_by"] = ""
        with self.assertRaises(core.Blocked): core.validate_case(c)

    def test_unknown_source_for_step(self):
        c = case(); c["steps"][0]["source_id"] = "S99"
        with self.assertRaises(core.Blocked): core.validate_case(c)

    def test_no_business_assertion(self):
        c = case(); c["steps"] = [{"method": "LoadGrid", "kwargs": {}, "source_id": "S1"}]
        with self.assertRaises(core.Blocked): core.validate_case(c)

    def test_private_unknown_mutating_methods_blocked(self):
        for method in ["capture_screen_state", "CaptureScreenState", "SetValue", "RunSQL", "eval"]:
            with self.subTest(method=method), self.assertRaises(core.Blocked):
                c = case(); c["steps"][0]["method"] = method; core.validate_case(c)

    def test_destructive_buttons_and_submenus_blocked(self):
        for kwargs in [{"button": "Salvar"}, {"button": "Excluir"},
                       {"button": "Visualizar", "sub_item": "Excluir"}]:
            with self.subTest(kwargs=kwargs), self.assertRaises(core.Blocked):
                core.validate_step({"method": "SetButton", "kwargs": kwargs, "source_id": "S1"})

    def test_ifexists_expected_must_be_boolean(self):
        with self.assertRaises(core.Blocked):
            core.validate_step({"method": "IfExists", "kwargs": {"string": "x"}, "expected": "true", "source_id": "S1"})

    def test_checkresult_not_boolean_protocol(self):
        step = {"method": "CheckResult", "kwargs": {"field": "CODE", "user_value": "1"}, "source_id": "S1"}
        core.validate_step(step)
        step["expected"] = True
        with self.assertRaises(core.Blocked): core.validate_step(step)

    def test_invalid_positions(self):
        for value in [False, -1, "1"]:
            with self.subTest(value=value), self.assertRaises(core.Blocked):
                c = case(); c["steps"][0]["kwargs"]["line"] = value; core.validate_case(c)

    def test_secret_detection_nested(self):
        with self.assertRaises(core.Blocked): core.check_secrets({"data": [{"password": "x"}]})

    def test_data_is_not_code(self):
        c = case(); c["steps"][0]["expected"] = "'); __import__('os').system('BAD'); #"
        tree = ast.parse(core.render_test(c, profile()))
        calls = [x for x in ast.walk(tree) if isinstance(x, ast.Call)]
        self.assertEqual(calls, [])

    def test_source_preserves_cp1252(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "legacy.prw"; original = '// Ação\nUser Function ZTEST()\nReturn'.encode("cp1252")
            p.write_bytes(original)
            result = core.inspect_sources([p], "cp1252")
            self.assertEqual(p.read_bytes(), original)
            self.assertEqual(result[0]["symbols"], ["ZTEST"])
            with self.assertRaises(UnicodeDecodeError): core.inspect_sources([p], "utf-8")

    def test_duplicate_json_keys(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "x.json"; p.write_text('{"a":1,"a":2}')
            with self.assertRaises(core.Blocked): core.load_json(p)

    def test_nonfinite_json(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "x.json"; p.write_text('{"a":NaN}')
            with self.assertRaises(core.Blocked): core.load_json(p)


class BundleTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name); self.bundle = self.root / "bundle"
        self.manifest = core.generate(case(), profile(), self.bundle)

    def test_generation_deterministic(self):
        other = core.generate(case(), profile(), self.root / "other")
        self.assertEqual(other, self.manifest)

    def test_integrity_roundtrip(self):
        self.assertEqual(core.verify_bundle(self.bundle)[2], self.manifest)

    def test_no_overwrite(self):
        with self.assertRaises(core.Blocked): core.generate(case(), profile(), self.bundle)

    def test_changed_test_blocked(self):
        (self.bundle / "test_case.py").write_text("raise RuntimeError('malicious')")
        with self.assertRaises(core.Blocked): core.verify_bundle(self.bundle)

    def test_changed_spec_and_manifest_blocked(self):
        c = case(); c["steps"][0]["expected"] = "changed"
        (self.bundle / "case.json").write_bytes(core.encoded(c))
        with self.assertRaises(core.Blocked): core.verify_bundle(self.bundle)

    def test_generated_script_cannot_start_erp_directly(self):
        with self.assertRaises(core.Blocked): runner.CaseTest("test_case").setUp()

    def test_approval_valid(self):
        core.approve(policy(self.manifest), case(), profile(), self.manifest)

    def test_approval_hashes(self):
        for key in ["bundle_sha256", "engine_sha256"]:
            with self.subTest(key=key), self.assertRaises(core.Blocked):
                p = policy(self.manifest); p[key] = "0" * 64
                core.approve(p, case(), profile(), self.manifest)

    def test_approval_expiry(self):
        for value in [(datetime.now(timezone.utc)-timedelta(seconds=10)).isoformat(),
                      (datetime.now(timezone.utc)+timedelta(days=5)).isoformat(), "2026-10-01T12:00:00"]:
            with self.subTest(value=value), self.assertRaises(core.Blocked):
                p = policy(self.manifest); p["expires_at"] = value
                core.approve(p, case(), profile(), self.manifest)

    def test_policy_target_mismatch(self):
        p = policy(self.manifest); p["target"]["branch"] = "OTHER"
        with self.assertRaises(core.Blocked): core.approve(p, case(), profile(), self.manifest)

    def test_policy_safety_controls(self):
        for key in ["integrations_blocked", "least_privilege_confirmed"]:
            with self.subTest(key=key), self.assertRaises(core.Blocked):
                p = policy(self.manifest); p[key] = False
                core.approve(p, case(), profile(), self.manifest)

    def test_button_requires_separate_authorization(self):
        c = case(); c["steps"].insert(0, {"method": "SetButton", "kwargs": {"button": "Visualizar"}, "source_id": "S1"})
        m = core.bundle_manifest(core.bundle_files(c, profile()))
        p = policy(m); p["allowed_buttons"] = []
        with self.assertRaises(core.Blocked): core.approve(p, c, profile(), m)

    def test_static_preflight_no_tir_import(self):
        with patch.dict(sys.modules, {"tir": None}), patch.object(core.importlib.metadata, "version", side_effect=importlib.metadata.PackageNotFoundError):
            result = core.preflight(profile())
        self.assertEqual(result["status"], "BLOCKED")
        self.assertFalse(result["network_checked"])

    def test_cli_validate_returns_success_without_execution(self):
        with contextlib.redirect_stdout(io.StringIO()) as capture:
            code = main("validate", ["--case", str(self.bundle / "case.json"), "--profile", str(self.bundle / "profile.json")])
        self.assertEqual(code, 0); self.assertFalse(json.loads(capture.getvalue())["erp_validated"])

    def test_cli_preflight_blocked_exit(self):
        with contextlib.redirect_stdout(io.StringIO()), patch.object(core.importlib.metadata, "version", side_effect=importlib.metadata.PackageNotFoundError):
            code = main("preflight", ["--profile", str(self.bundle / "profile.json")])
        self.assertEqual(code, 2)

    def test_no_execute_flag_no_side_effect(self):
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            main("run", ["--bundle", str(self.bundle), "--policy", "none", "--output", str(self.root / "run")])
        self.assertFalse((self.root / "run").exists())

    def test_preflight_blocks_before_process(self):
        p = self.root / "approval.json"; core.write_json(p, policy(self.manifest)); p.chmod(0o600)
        with patch.object(runner, "preflight", return_value={"status": "BLOCKED"}), patch.object(runner.subprocess, "Popen") as start:
            with self.assertRaises(core.Blocked): runner.execute(self.bundle, p, self.root / "run")
            start.assert_not_called()

    def test_simulated_worker_pass_not_erp_validation(self):
        r, helper = self._worker()
        self.assertEqual(r["status"], "PASS"); self.assertFalse(r["erp_validated"])
        self.assertEqual(r["execution_mode"], "simulated")
        self.assertEqual(helper.calls[-1], "TearDown")

    def test_simulated_wrong_value_fails(self):
        r, _ = self._worker(value="wrong")
        self.assertEqual(r["status"], "FAIL")

    def test_simulated_no_image_not_pass(self):
        r, _ = self._worker(image=False)
        self.assertEqual(r["status"], "ERROR")

    def test_simulated_teardown_error_not_pass(self):
        r, _ = self._worker(teardown_error=True)
        self.assertEqual(r["status"], "ERROR")

    def test_simulated_identity_mismatch_no_program(self):
        r, helper = self._worker(identity=False)
        self.assertNotEqual(r["status"], "PASS")
        self.assertFalse(any(isinstance(c, tuple) and c[0] == "Program" for c in helper.calls))

    def test_simulated_native_error_not_pass(self):
        r, _ = self._worker(native_error=True)
        self.assertNotEqual(r["status"], "PASS")

    def test_grid_check_is_flushed(self):
        c = case(); c["steps"] = [{"method": "CheckResult", "kwargs": {"field": "CODE", "user_value": "000001 ", "grid": True}, "source_id": "S1"}]
        r, h = self._worker(custom_case=c)
        self.assertEqual(r["status"], "PASS")
        i = h.calls.index("CheckResult"); self.assertEqual(h.calls[i+1:i+3], ["LoadGrid", "AssertTrue"])

    def test_padding_not_trimmed(self):
        r, _ = self._worker(value="000001")
        self.assertEqual(r["status"], "FAIL")

    def test_bool_not_equal_to_integer(self):
        c = case(); c["steps"][0]["expected"] = True
        r, _ = self._worker(custom_case=c, value=1)
        self.assertEqual(r["status"], "FAIL")

    def _worker(self, custom_case=None, **fake_options):
        private = self.root / "worker"; private.mkdir()
        images = private / "screenshots"; images.mkdir()
        m = core.generate(custom_case or case(), profile(), private / "bundle")
        core.write_json(private / "runtime.json", {"config_path": "FAKE_NO_CONNECTION",
                        "screenshots": str(images), "engine_sha256": core.engine_hash(),
                        "bundle_sha256": m["bundle_sha256"]})
        helper = FakeHelper(images, **fake_options)
        code = runner.run_worker(private, factory=lambda _: helper)
        result = core.load_json(private / "worker-result.json")
        self.assertEqual(code, 0 if result["status"] == "PASS" else 1)
        return result, helper


class EvidenceTests(unittest.TestCase):
    def test_evidence_integrity_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d); core.write_json(p / "result.json", {"status": "ERROR", "run_id": "r1"})
            result = runner.collect(p, create=True)
            self.assertFalse(result["uploaded"])
            runner.collect(p)
            (p / "result.json").write_text('{"status":"PASS","run_id":"r1"}')
            with self.assertRaises(core.Blocked): runner.collect(p)

    def test_private_files_not_collected(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d); (p / ".private").mkdir(); (p / ".private" / "x").write_text("secret")
            with self.assertRaises(core.Blocked): runner.artifacts(p)

    def test_redaction(self):
        self.assertEqual(runner.scrub({"x": ["user secret"]}, ("user", "secret")), {"x": ["[REDACTED] [REDACTED]"]})

    def test_symlink_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d); target = p / "target"; target.write_text("data")
            link = p / "link"
            try: link.symlink_to(target)
            except OSError: self.skipTest("Platform does not permit symlink creation for test user")
            with self.assertRaises(core.Blocked): runner.artifacts(p)


if __name__ == "__main__":
    unittest.main()
