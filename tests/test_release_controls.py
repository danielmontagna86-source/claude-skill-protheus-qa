"""Release, archive and authorization controls. No external service calls."""
import io
import tempfile
import subprocess
import os
import sys
import unittest
import warnings
import zipfile
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import tirqa_runner as runner
import tirqa_core as core
import package_skill
from verify_distribution import verify_archive
from verify_release_assets import verify_metadata
from test_tirqa import case, profile, policy


class ReleaseControls(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "VERSION").write_text("0.2.0-rc.3\n")
        (self.root / "README.md").write_text("Synthetic packaging fixture\n")
        with patch("sys.stdout", new_callable=io.StringIO):
            self.archive = package_skill.build_zip(self.root)
        self.data = self.archive.read_bytes()

    def modified(self, name, value=b"changed", duplicate=False, mode=0o100644):
        buffer = io.BytesIO()
        with zipfile.ZipFile(io.BytesIO(self.data)) as original, zipfile.ZipFile(buffer, "w") as target:
            for info in original.infolist():
                if info.filename == name and not duplicate: continue
                target.writestr(info, original.read(info.filename))
            item = zipfile.ZipInfo(name); item.create_system = 3; item.external_attr = mode << 16
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", UserWarning)
                target.writestr(item, value)
        return buffer.getvalue()

    def test_real_owned_process_is_stopped(self):
        options = ({"creationflags": subprocess.CREATE_NEW_PROCESS_GROUP} if os.name == "nt"
                   else {"start_new_session": True})
        process = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(60)"], **options)
        try:
            runner.stop_tree(process)
            self.assertIsNotNone(process.poll())
        finally:
            if process.poll() is None:
                process.kill(); process.wait(timeout=10)

    def test_distribution_valid(self):
        self.assertEqual(verify_archive(self.data)["status"], "VERIFIED")

    def test_package_tamper_rejected(self):
        with self.assertRaises(core.Blocked): verify_archive(self.modified("testing-protheus-routines/README.md"))

    def test_extra_package_file_rejected(self):
        with self.assertRaises(core.Blocked): verify_archive(self.modified("testing-protheus-routines/extra.txt"))

    def test_duplicate_package_file_rejected(self):
        with self.assertRaises(core.Blocked): verify_archive(self.modified("testing-protheus-routines/README.md", duplicate=True))

    def test_archive_path_traversal_rejected(self):
        with self.assertRaises(core.Blocked): verify_archive(self.modified("../escape.py"))

    def test_archive_symlink_rejected(self):
        with self.assertRaises(core.Blocked): verify_archive(self.modified("testing-protheus-routines/link", mode=0o120777))

    def metadata(self):
        return {"tag_name": "v0.2.0-rc.3", "target_commitish": "a"*40, "draft": False, "prerelease": True,
                "assets": [{"name": self.archive.name, "state": "uploaded", "size": len(self.data),
                            "digest": "sha256:"+core.digest(self.data),
                            "browser_download_url": "https://github.com/owner/repo/releases/download/v0.2.0-rc.3/"+self.archive.name}]}

    def test_release_metadata_matches_exact_artifact(self):
        self.assertEqual(len(verify_metadata(self.metadata(), "owner/repo", "v0.2.0-rc.3", "a"*40, [self.archive])), 1)

    def test_release_wrong_commit_blocked(self):
        value = self.metadata(); value["target_commitish"] = "b"*40
        with self.assertRaises(core.Blocked): verify_metadata(value, "owner/repo", "v0.2.0-rc.3", "a"*40, [self.archive])

    def test_release_missing_asset_blocked(self):
        value = self.metadata(); value["assets"] = []
        with self.assertRaises(core.Blocked): verify_metadata(value, "owner/repo", "v0.2.0-rc.3", "a"*40, [self.archive])

    def test_release_changed_digest_blocked(self):
        value = self.metadata(); value["assets"][0]["digest"] = "sha256:"+"0"*64
        with self.assertRaises(core.Blocked): verify_metadata(value, "owner/repo", "v0.2.0-rc.3", "a"*40, [self.archive])

    def test_deep_json_is_structured_block(self):
        with self.assertRaises(core.Blocked): core.parse_json(b'{"x":'+b'['*4000+b'0'+b']'*4000+b'}')

    def test_dependency_risk_not_self_approved(self):
        manifest = core.bundle_manifest(core.bundle_files(case(), profile()))
        value = policy(manifest); value["dependency_risks_reviewed"] = False
        with self.assertRaisesRegex(core.Blocked, "dependency_risk_review_required"):
            core.approve(value, case(), profile(), manifest)


if __name__ == "__main__": unittest.main()
