"""Test documented PowerShell installation in a disposable project, using local ZIP fixtures.

No HTTP download, ERP, real project, global installation or credential is used.
This is a development check, not an installer for the user's workstation.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from tirqa_core import require, write_json
from verify_distribution import verify_archive


def verify_copy(destination: Path, manifest: dict) -> int:
    require(destination.is_dir(), "documented_destination_missing")
    for name, expected in manifest["files"].items():
        require(hashlib.sha256((destination / name).read_bytes()).hexdigest() == expected,
                "installed_file_differs_from_package")
    return len(manifest["files"])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--zip", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    require(os.name == "nt", "windows_check_only")
    shell = shutil.which("pwsh")
    require(shell is not None, "powershell_required")
    root = Path(__file__).resolve().parents[1]
    blocks = re.findall(r"```powershell\n(.*?)```", (root / "INSTALL.md").read_text(encoding="utf-8"), re.S)
    require(len(blocks) == 3, "unexpected_installation_blocks")
    data = args.zip.read_bytes(); package = verify_archive(data)
    outputs = []
    with tempfile.TemporaryDirectory(prefix="qa-install-review-") as temp:
        base = Path(temp); fixtures = base / "fixtures"; fixtures.mkdir()
        fixture_zip = fixtures / "testing-protheus-routines.zip"; fixture_zip.write_bytes(data)
        checksums = fixtures / "SHA256SUMS.txt"
        checksums.write_text(package["sha256"] + "  testing-protheus-routines.zip\n", encoding="utf-8")
        # Documented commands are executed verbatim, except the explicitly chosen agent.
        prelude = r'''
$ErrorActionPreference = 'Stop'
function Invoke-WebRequest {
  param([switch]$UseBasicParsing, [string]$Uri, [string]$OutFile)
  if ($Uri -notmatch '^https://github\.com/danielmontagna86-source/claude-skill-protheus-qa/releases/download/v[0-9.]+-rc\.[0-9]+/(testing-protheus-routines\.zip|SHA256SUMS\.txt)$') { throw 'Unexpected test download' }
  Copy-Item -LiteralPath (Join-Path $env:QA_FIXTURES ([IO.Path]::GetFileName($Uri))) -Destination $OutFile
}
'''
        for agent in ("claude", "codex"):
            project = base / ("Project with spaces " + agent); project.mkdir()
            stage = base / ("temp-" + agent); stage.mkdir()
            env = dict(os.environ, QA_FIXTURES=str(fixtures), TEMP=str(stage), TMP=str(stage))
            copy_block = blocks[1].replace("$Agent = 'claude'", "$Agent = '" + agent + "'")
            script = base / (agent + ".ps1")
            body = prelude + blocks[0] + "\n" + copy_block + r'''
$before = (Get-FileHash -LiteralPath (Join-Path $Destination 'SKILL.md')).Hash
$refused = $false
try {
'''+ copy_block + r'''
} catch { $refused = $true }
if (-not $refused) { throw 'Existing installation was not refused' }
if ((Get-FileHash -LiteralPath (Join-Path $Destination 'SKILL.md')).Hash -ne $before) { throw 'Existing installation changed' }
'''
            script.write_text(body, encoding="utf-8-sig")
            done = subprocess.run([shell, "-NoProfile", "-NonInteractive", "-File", str(script)],
                                  cwd=project, env=env, capture_output=True, text=True, timeout=90)
            require(done.returncode == 0, "documented_powershell_install_failed:" + agent)
            parent = ".claude" if agent == "claude" else ".agents"
            destination = project / parent / "skills" / "testing-protheus-routines"
            manifest = json.loads((destination / "PACKAGE_MANIFEST.json").read_text(encoding="utf-8"))
            count = verify_copy(destination, manifest)
            require((destination / "VERSION").read_text().strip() == package["version"], "installed_version_drift")
            outputs.append({"agent": agent, "status": "PASS", "files_verified": count,
                            "existing_destination_refused": True})
        # A bad checksum must interrupt the first real documentation block.
        checksums.write_text("0" * 64 + "  testing-protheus-routines.zip\n", encoding="utf-8")
        project = base / "bad-checksum-project"; project.mkdir()
        script = base / "bad-checksum.ps1"; script.write_text(prelude + blocks[0], encoding="utf-8-sig")
        done = subprocess.run([shell, "-NoProfile", "-NonInteractive", "-File", str(script)],
                              cwd=project, env=env, capture_output=True, text=True, timeout=90)
        require(done.returncode != 0 and "Checksum divergente" in done.stderr,
                "bad_checksum_not_rejected")
        require(not any(project.iterdir()), "bad_checksum_modified_project")
        outputs.append({"scenario": "bad_checksum", "status": "PASS", "installation_blocked": True})
    report = {"status": "PASS", "scope": "documented_copy_flow_local_fixtures", "checks": outputs,
              "package_sha256": package["sha256"], "http_download_performed": False,
              "ai_client_discovery_tested": False, "erp_validated": False}
    args.output.parent.mkdir(parents=True, exist_ok=True); write_json(args.output, report)
    print(json.dumps(report, indent=2)); return 0


if __name__ == "__main__": raise SystemExit(main())
