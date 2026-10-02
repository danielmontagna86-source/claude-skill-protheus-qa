"""Explicit CI-only installation/import probe and dependency risk report; no ERP login."""
from __future__ import annotations
import argparse
import importlib.metadata
import inspect
import json
import os
import socket
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch
from tirqa_core import TIR_VERSION, require, write_json, load_json, digest
from verify_tir_api import verify


def probe(output: Path) -> None:
    require(sys.version_info[:2] == (3, 12), "python_312_required")
    require(importlib.metadata.version("tir_framework") == TIR_VERSION, "tir_version_mismatch")
    # Imports must not start a browser, other subprocess or network connection.
    with patch.object(socket.socket, "connect", side_effect=RuntimeError("network_on_import")), \
         patch.object(socket, "create_connection", side_effect=RuntimeError("network_on_import")), \
         patch.object(subprocess, "Popen", side_effect=RuntimeError("subprocess_on_import")):
        from tir import Webapp
    source = Path(inspect.getsourcefile(Webapp)).read_bytes()
    contract = verify(source.replace(b"\r\n", b"\n"))
    write_json(output, {"status": "IMPORT_AND_SOURCE_VERIFIED", "python": sys.version.split()[0],
                        "tir": TIR_VERSION, "requests": importlib.metadata.version("requests"),
                        "source_contract": contract, "browser_started": False, "erp_validated": False})


def environment_python(path: Path) -> Path:
    return path / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


def install_and_audit(work: Path, output: Path) -> None:
    require(not work.exists(), "audit_workdir_exists")
    work.mkdir(parents=True); output.mkdir(parents=True, exist_ok=True)
    runtime, auditor = work / "runtime", work / "auditor"
    for directory in (runtime, auditor):
        subprocess.run([sys.executable, "-m", "venv", str(directory)], check=True, timeout=120)
    runtime_python, audit_python = environment_python(runtime), environment_python(auditor)
    subprocess.run([str(runtime_python), "-m", "pip", "install", "--disable-pip-version-check",
                    "tir-framework==" + TIR_VERSION], check=True, timeout=600)
    subprocess.run([str(runtime_python), "-m", "pip", "check"], check=True, timeout=120)
    subprocess.run([str(runtime_python), str(Path(__file__).resolve()), "--probe-only",
                    "--output-dir", str(output.resolve())], check=True, timeout=120)
    freeze = subprocess.run([str(runtime_python), "-m", "pip", "freeze"], check=True,
                            capture_output=True, text=True, timeout=60).stdout
    resolved = output / "runtime-resolved.txt"
    resolved.write_bytes(freeze.replace("\r\n", "\n").encode("utf-8"))
    subprocess.run([str(audit_python), "-m", "pip", "install", "--disable-pip-version-check",
                    "pip-audit==2.10.1"], check=True, timeout=600)
    audit_path = output / "dependency-audit.json"
    audit = subprocess.run([str(audit_python), "-m", "pip_audit", "--no-deps", "--disable-pip",
                            "--progress-spinner", "off", "--timeout", "30", "-r", str(resolved),
                            "--format", "json", "--desc", "off", "--aliases", "on", "--output", str(audit_path)],
                           timeout=300, check=False)
    report = load_json(audit_path)
    dependencies = report.get("dependencies")
    require(isinstance(dependencies, list) and bool(dependencies), "audit_report_missing_dependencies")
    findings = sum(len(d.get("vulns", [])) for d in dependencies)
    skipped = [d.get("name") for d in dependencies if d.get("skip_reason")]
    require(audit.returncode in {0, 1} and ((audit.returncode == 0) == (findings == 0)), "audit_execution_failed")
    summary = {"status": "VULNERABILITIES_FOUND" if findings else ("INCOMPLETE_AUDIT" if skipped else "NO_KNOWN_FINDINGS"),
               "findings": findings, "packages": len(dependencies), "skipped_packages": skipped,
               "audit_exit_code": audit.returncode, "auditor": "pip-audit 2.10.1",
               "requirements_sha256": digest(resolved.read_bytes()),
               "execution_security_approved": False, "erp_validated": False,
               "note": "Report completion is not a clean security approval; operator risk review remains required."}
    write_json(output / "dependency-summary.json", summary)
    print(json.dumps(summary, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--install-and-audit", action="store_true")
    mode.add_argument("--probe-only", action="store_true")
    parser.add_argument("--work-dir", type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    if args.probe_only:
        probe(args.output_dir / "runtime-probe.json")
    else:
        require(args.work_dir is not None, "audit_workdir_required")
        install_and_audit(args.work_dir.resolve(), args.output_dir.resolve())


if __name__ == "__main__": main()
