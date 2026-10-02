"""Build a reproducible skill ZIP with an internal SHA-256 inventory. No run data."""
from __future__ import annotations
import hashlib
import json
import sys
import zipfile
from pathlib import Path
from validate_skill import SKILL_NAME, validate
from validate_tir_release import validate as validate_release

EXCLUDED_DIRS = {".git", ".github", ".venv", "venv", "__pycache__", ".pytest_cache",
                 "dist", ".private", "artifacts", "evidence", "qa-work", "reports", "screenshots", "logs", "runs", "bundles"}
INCLUDED_DIRS = {"references", "routines", "templates", "examples", "evals", "scripts",
                 "tests", "RELEASE_NOTES", ".claude-plugin"}
ROOT_FILES = {"SKILL.md", "README.md", "INSTALL.md", "INSTALL_WITH_AI.md", "USAGE.md", "USAGE_WITH_AI.md", "CHANGELOG.md", "VERSION",
              "LICENSE", "SKILL_MANIFEST.md", "MARKETPLACE.md", "TIR_QUICKSTART.md", "SECURITY.md", "requirements-tir.txt", ".gitattributes"}


def collect_files(root: Path) -> list[Path]:
    selected = []
    for path in root.rglob("*"):
        rel = path.relative_to(root)
        if any(x in EXCLUDED_DIRS for x in rel.parts): continue
        if path.is_symlink(): raise ValueError("Symlinks must not be packaged")
        if not path.is_file() or path.suffix in {".pyc", ".pyo"}: continue
        if len(rel.parts) == 1 and path.name not in ROOT_FILES: continue
        if len(rel.parts) > 1 and rel.parts[0] not in INCLUDED_DIRS: continue
        if path.name.startswith(".env") or path.name in {"config.json", "approval.json", "result.json"}:
            raise ValueError("Runtime or secret-bearing filename inside the distributable")
        selected.append(path)
    return sorted(selected)


def canonical_bytes(path: Path) -> bytes:
    content = path.read_bytes()
    # Normalize only project-maintained text, never user ADVPL/TLPP source bytes.
    if path.suffix in {".py", ".md", ".json", ".txt", ".yml", ".yaml"} or path.name in {"VERSION", "LICENSE", ".gitattributes"}:
        return content.replace(b"\r\n", b"\n")
    return content


def build_zip(root: Path) -> Path:
    output = root / "dist"; output.mkdir(exist_ok=True)
    target = output / f"{SKILL_NAME}.zip"
    files = {p.relative_to(root).as_posix(): canonical_bytes(p) for p in collect_files(root)}
    manifest = {"skill": SKILL_NAME, "version": (root / "VERSION").read_text().strip(),
                "files": {name: hashlib.sha256(data).hexdigest() for name, data in files.items()}}
    files["PACKAGE_MANIFEST.json"] = (json.dumps(manifest, sort_keys=True, indent=2) + "\n").encode()
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_STORED) as archive:
        for name, data in sorted(files.items()):
            info = zipfile.ZipInfo(f"{SKILL_NAME}/{name}", date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_STORED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)
    with zipfile.ZipFile(target) as archive:
        if archive.testzip() is not None: raise ValueError("ZIP verification failed")
    checksum = hashlib.sha256(target.read_bytes()).hexdigest()
    (output / "SHA256SUMS.txt").write_text(f"{checksum}  {target.name}\n", encoding="utf-8")
    print(f"Package: {target}; files: {len(files)}; SHA256: {checksum}")
    return target


def main() -> int:
    errors, warnings = validate()
    errors += validate_release()
    for warning in warnings: print("WARNING: " + warning, file=sys.stderr)
    if errors:
        for error in errors: print(error, file=sys.stderr)
        return 1
    build_zip(Path(__file__).resolve().parents[1])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
