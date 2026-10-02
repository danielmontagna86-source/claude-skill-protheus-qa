"""Additional failure-injection tests for the parent executor, without a real ERP."""
import contextlib
import io
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import tirqa_core as core
import tirqa_runner as runner
from tirqa_cli import main
from test_tirqa import case, profile, policy, FakeHelper


class ParentRunnerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name); self.bundle = self.root / "bundle"
        self.manifest = core.generate(case(), profile(), self.bundle)
        self.approval = self.root / "approval.json"
        core.write_json(self.approval, policy(self.manifest)); self.approval.chmod(0o600)
        self.output = self.root / "run"

    def test_private_directory_real_platform_controls(self):
        # Exercise actual POSIX permissions / Windows ACL provisioning separately
        # from parent-worker tests that intentionally mock subprocess.Popen.
        path = self.root / "restricted"
        runner.private_directory(path)
        self.assertTrue(path.is_dir())
        if os.name != "nt":
            self.assertEqual(path.stat().st_mode & 0o777, 0o700)
        with self.assertRaises(core.Blocked):
            runner.private_directory(path)

    def test_missing_credentials_no_process(self):
        with patch.object(runner, "preflight", return_value={"status": "READY_FOR_AUTHORIZATION"}), patch.dict(os.environ, {}, clear=True), patch.object(runner.subprocess, "Popen") as spawn:
            with self.assertRaisesRegex(core.Blocked, "credentials_missing"):
                runner.execute(self.bundle, self.approval, self.output)
            spawn.assert_not_called()
        self.assertFalse(self.output.exists())

    def test_approval_inside_bundle_rejected(self):
        inside = self.bundle / "approval.json"; inside.write_bytes(self.approval.read_bytes())
        with self.assertRaisesRegex(core.Blocked, "external_policy_required"):
            runner.execute(self.bundle, inside, self.output)

    def test_unsafe_policy_permissions_rejected(self):
        if os.name == "nt":
            # Windows uses explicit operator-maintained ACLs, documented separately.
            self.assertEqual(os.name, "nt"); return
        self.approval.chmod(0o666)
        with self.assertRaisesRegex(core.Blocked, "policy_must_not_be_group_world_writable"):
            runner.execute(self.bundle, self.approval, self.output)

    def test_worker_exits_zero_without_result_not_pass(self):
        process = type("FakeProcess", (), {"wait": lambda self, **kw: 0, "poll": lambda self: 0})()
        with patch.object(runner, "preflight", return_value={"status": "READY_FOR_AUTHORIZATION"}), patch.dict(os.environ, {"TIR_USER": "qa_user", "TIR_PASSWORD": "test_secret"}), patch.object(runner, "private_directory", side_effect=lambda path: path.mkdir(parents=True, mode=0o700)), patch.object(runner.subprocess, "Popen", return_value=process) as spawn:
            result = runner.execute(self.bundle, self.approval, self.output)
        self.assertEqual(result["status"], "ERROR")
        self.assertFalse(result["erp_validated"])
        self.assertFalse((self.output / ".private").exists())
        args = spawn.call_args.args[0]
        self.assertEqual(args[1], "-I")
        self.assertNotIn("test_secret", " ".join(args))
        self.assertNotIn("TIR_PASSWORD", spawn.call_args.kwargs["env"])
        self.assertEqual(runner.collect(self.output)["status"], "ERROR")

    def test_spawn_failure_removes_temporary_credentials(self):
        with patch.object(runner, "preflight", return_value={"status": "READY_FOR_AUTHORIZATION"}), patch.dict(os.environ, {"TIR_USER": "qa_user", "TIR_PASSWORD": "test_secret"}), patch.object(runner, "private_directory", side_effect=lambda path: path.mkdir(parents=True, mode=0o700)), patch.object(runner.subprocess, "Popen", side_effect=OSError("failure test_secret")):
            result = runner.execute(self.bundle, self.approval, self.output)
        self.assertEqual(result["status"], "ERROR")
        self.assertFalse((self.output / ".private").exists())
        self.assertNotIn("test_secret", (self.output / "result.json").read_text())

    def test_tir_not_imported_by_cli_help(self):
        before = set(sys.modules)
        with contextlib.redirect_stdout(io.StringIO()), self.assertRaises(SystemExit):
            main("generate", ["--help"])
        self.assertNotIn("tir", set(sys.modules) - before)


class OutcomeTests(unittest.TestCase):
    def test_zero_tests_cannot_be_collected_as_pass(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            core.write_json(root / "result.json", {"status": "PASS", "run_id": "invalid", "counts": {"tests": 0, "failures": 0, "errors": 0, "skipped": 0}})
            with self.assertRaisesRegex(core.Blocked, "invalid_pass_evidence"):
                runner.collect(root, create=True)

    def test_skipped_test_cannot_be_collected_as_pass(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            core.write_json(root / "result.json", {"status": "PASS", "run_id": "invalid", "counts": {"tests": 1, "failures": 0, "errors": 0, "skipped": 1}})
            with self.assertRaisesRegex(core.Blocked, "invalid_pass_evidence"):
                runner.collect(root, create=True)

    def test_skipped_worker_not_pass(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); images = root / "screenshots"; images.mkdir()
            manifest = core.generate(case(), profile(), root / "bundle")
            core.write_json(root / "runtime.json", {"config_path": "FAKE", "screenshots": str(images), "engine_sha256": core.engine_hash(), "bundle_sha256": manifest["bundle_sha256"]})
            helper = FakeHelper(images)
            with patch.object(helper, "GetValue", side_effect=unittest.SkipTest("simulated skip")):
                code = runner.run_worker(root, factory=lambda _: helper)
            result = core.load_json(root / "worker-result.json")
            self.assertNotEqual(code, 0); self.assertNotEqual(result["status"], "PASS")
            self.assertEqual(result["counts"]["skipped"], 1)
            self.assertFalse(result["erp_validated"])

    def test_bad_upstream_blob_blocked_without_execution(self):
        from verify_tir_api import verify
        with self.assertRaisesRegex(core.Blocked, "official_source_blob_mismatch"):
            verify(b"print('never executed')")


if __name__ == "__main__": unittest.main()
