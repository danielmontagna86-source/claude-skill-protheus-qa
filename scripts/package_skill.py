#!/usr/bin/env python3
"""Build the official Claude Skill ZIP package.

The repository may have a different name, but the ZIP must contain a top-level
folder named exactly like the skill declared in SKILL.md: testing-protheus-routines.
"""

from __future__ import annotations

import sys
import zipfile
from pathlib import Path

from validate_skill import SKILL_NAME, validate

OUTPUT_DIR = "dist"
OUTPUT_ZIP = f"{SKILL_NAME}.zip"

EXCLUDED_DIRS = {
    ".git",
    ".github",
    ".pytest_cache",
    ".venv",
    "__pycache__",
    OUTPUT_DIR,
}

EXCLUDED_FILE_SUFFIXES = {
    ".pyc",
    ".pyo",
    ".DS_Store",
}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def should_include(path: Path, root: Path) -> bool:
    rel = path.relative_to(root)

    if any(part in EXCLUDED_DIRS for part in rel.parts):
        return False

    if path.name in EXCLUDED_FILE_SUFFIXES:
        return False

    if any(path.name.endswith(suffix) for suffix in EXCLUDED_FILE_SUFFIXES):
        return False

    return path.is_file()


def collect_files(root: Path) -> list[Path]:
    return sorted(path for path in root.rglob("*") if should_include(path, root))


def build_zip(root: Path) -> Path:
    output_dir = root / OUTPUT_DIR
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / OUTPUT_ZIP
    if output_path.exists():
        output_path.unlink()

    files = collect_files(root)

    with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for file_path in files:
            rel = file_path.relative_to(root)
            archive_name = Path(SKILL_NAME) / rel
            archive.write(file_path, archive_name.as_posix())

    print(f"Package created: {output_path}")
    print(f"Top-level folder inside ZIP: {SKILL_NAME}/")
    print(f"Files packaged: {len(files)}")
    return output_path


def main() -> int:
    errors, warnings = validate()

    for warning in warnings:
        print(f"WARNING: {warning}", file=sys.stderr)

    if errors:
        print("Package aborted because validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    build_zip(repo_root())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
