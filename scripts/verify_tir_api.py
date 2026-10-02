"""Verify the supported public API against the exact official TIR source blob."""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
from pathlib import Path
from urllib.request import urlopen

from tirqa_core import API, Blocked, TIR_COMMIT, require

BLOB_SHA = "082afe46702649276d994ea1e783e6e27cc6eef2"
URL = f"https://raw.githubusercontent.com/totvs/tir/{TIR_COMMIT}/tir/main.py"
LIFECYCLE = {"__init__": {"config_path", "autostart"}, "Start": set(), "TearDown": set(),
             "Setup": {"initial_program", "date", "group", "branch", "module"},
             "Program": {"program_name"}, "Screenshot": {"filename"}, "AssertTrue": set()}


def verify(source: bytes) -> dict:
    blob = hashlib.sha1(b"blob " + str(len(source)).encode("ascii") + b"\0" + source).hexdigest()
    require(blob == BLOB_SHA, "official_source_blob_mismatch")
    tree = ast.parse(source.decode("utf-8"))
    cls = next((x for x in tree.body if isinstance(x, ast.ClassDef) and x.name == "Webapp"), None)
    require(cls is not None, "webapp_class_missing")
    methods = {x.name: x for x in cls.body if isinstance(x, ast.FunctionDef)}
    expected = {name: allowed for name, (_, allowed) in API.items()} | LIFECYCLE
    for name, params in expected.items():
        require(name in methods, "public_method_missing:" + name)
        actual = {arg.arg for arg in methods[name].args.args + methods[name].args.kwonlyargs}
        require(params <= actual, "public_signature_mismatch:" + name)
    require(not any(isinstance(n, ast.Return) and n.value is not None
                    for n in ast.walk(methods["CheckResult"])), "checkresult_semantics_changed")
    return {"status": "VERIFIED", "commit": TIR_COMMIT, "blob": blob,
            "public_methods_checked": len(expected), "tir_imported": False,
            "erp_validated": False}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    inputs = parser.add_mutually_exclusive_group(required=True)
    inputs.add_argument("--source", type=Path)
    inputs.add_argument("--fetch", action="store_true", help="Explicit network access to the pinned TOTVS URL only")
    args = parser.parse_args()
    try:
        if args.fetch:
            with urlopen(URL, timeout=30) as stream:
                source = stream.read(4_000_001)
        else:
            source = args.source.read_bytes()
        require(len(source) <= 4_000_000, "source_too_large")
        print(json.dumps(verify(source), indent=2))
        return 0
    except (Blocked, OSError, ValueError) as exc:
        print(json.dumps({"status": "BLOCKED", "reason": str(exc) if isinstance(exc, Blocked) else type(exc).__name__}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
