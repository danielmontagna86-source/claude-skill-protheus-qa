"""Shared CLI. Offline by default; only `run` may start a browser."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from tirqa_core import (Blocked, generate, inspect_sources, load_json, preflight,
                        validate_case, validate_profile)
from tirqa_runner import collect, execute


def main(command: str, argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    if command == "inspect":
        parser.add_argument("paths", nargs="+", type=Path)
        parser.add_argument("--encoding", required=True, choices=["utf-8", "utf-8-sig", "cp1252"])
    if command in {"validate", "generate"}:
        parser.add_argument("--case", required=True, type=Path)
    if command in {"validate", "generate", "preflight"}:
        parser.add_argument("--profile", required=True, type=Path)
    if command == "generate":
        parser.add_argument("--output", required=True, type=Path)
    if command == "run":
        parser.add_argument("--bundle", required=True, type=Path)
        parser.add_argument("--policy", required=True, type=Path)
        parser.add_argument("--output", required=True, type=Path)
        parser.add_argument("--execute", required=True, action="store_true",
                            help="Explicit intent; does not replace the external approval policy.")
    if command == "collect":
        parser.add_argument("--run-dir", required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        if command == "inspect":
            result = {"status": "READ_ONLY_ANALYSIS", "sources": inspect_sources(args.paths, args.encoding)}
        elif command == "validate":
            validate_case(load_json(args.case))
            validate_profile(load_json(args.profile))
            result = {"status": "READY_FOR_GENERATION", "erp_validated": False}
        elif command == "generate":
            result = generate(load_json(args.case), load_json(args.profile), args.output)
            result.update(status="GENERATED_NOT_EXECUTED", erp_validated=False)
        elif command == "preflight":
            result = preflight(load_json(args.profile))
        elif command == "run":
            result = execute(args.bundle, args.policy, args.output)
        elif command == "collect":
            result = collect(args.run_dir)
        else:
            raise Blocked("unknown_command")
        print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
        return 2 if result.get("status") in {"BLOCKED", "NOT_RUN", "SKIPPED"} else (
            1 if result.get("status") in {"FAIL", "ERROR"} else 0)
    except (Blocked, OSError, ValueError, KeyError, TypeError) as exc:
        # Do not echo arbitrary inputs, source contents, credentials or tracebacks to CI.
        reason = str(exc) if isinstance(exc, Blocked) else type(exc).__name__
        print(json.dumps({"status": "BLOCKED", "reason": reason, "erp_validated": False}))
        return 2


if __name__ == "__main__":
    raise SystemExit("Use one of the six documented entrypoints.")
