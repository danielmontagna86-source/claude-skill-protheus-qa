"""Execute all offline tests and emit a strict, machine-readable result."""
import argparse
import platform
import sys
import unittest
from pathlib import Path
from tirqa_core import write_json


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    suite = unittest.defaultTestLoader.discover(str(root / "tests"))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    counts = {"tests": result.testsRun, "failures": len(result.failures), "errors": len(result.errors),
              "skipped": len(result.skipped), "expected_failures": len(result.expectedFailures),
              "unexpected_successes": len(result.unexpectedSuccesses)}
    success = counts["tests"] > 0 and all(value == 0 for key, value in counts.items() if key != "tests")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    write_json(args.output, {"scope": "offline_tools_only", "status": "PASS" if success else "FAIL",
                            "python": platform.python_version(), "platform": sys.platform,
                            "counts": counts, "erp_validated": False})
    return 0 if success else 1


if __name__ == "__main__": raise SystemExit(main())
