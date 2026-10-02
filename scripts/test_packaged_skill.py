"""Re-run tests from the exact validated distribution, not only the checkout."""
import argparse
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
from verify_distribution import verify_archive


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--zip", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    verify_archive(args.zip.read_bytes())
    with tempfile.TemporaryDirectory(prefix="qa-distribution-") as temp:
        with zipfile.ZipFile(args.zip) as archive: archive.extractall(temp)
        root = Path(temp) / "testing-protheus-routines"
        return subprocess.run([sys.executable, str(root / "scripts/run_local_checks.py"),
                               "--output", str(args.output.resolve())], cwd=root, timeout=180).returncode


if __name__ == "__main__": raise SystemExit(main())
