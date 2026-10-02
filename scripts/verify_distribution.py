"""Validate a skill ZIP and optionally require a byte-identical cross-platform build."""
from __future__ import annotations
import argparse
import io
import json
import re
import unicodedata
import zipfile
from pathlib import Path, PurePosixPath
from tirqa_core import Blocked, digest, parse_json, require, write_json

SKILL = "testing-protheus-routines"


def verify_archive(data: bytes) -> dict:
    require(len(data) <= 20_000_000, "archive_too_large")
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        names = archive.namelist()
        require(len(names) == len(set(names)) and 1 < len(names) <= 5000, "duplicate_or_invalid_entries")
        total = 0
        portable_names = set()
        for info in archive.infolist():
            path = PurePosixPath(info.filename)
            require(not path.is_absolute() and ".." not in path.parts and "\\" not in info.filename
                    and len(path.parts) >= 2 and path.parts[0] == SKILL, "unsafe_archive_path")
            require(info.filename == "/".join(path.parts), "noncanonical_archive_path")
            for part in path.parts:
                require(part == unicodedata.normalize("NFC", part) and len(part) <= 255
                        and not part.endswith((".", " "))
                        and not any(ord(ch) < 32 or ch in '<>:"|?*' for ch in part),
                        "nonportable_archive_path")
                stem = part.split(".")[0].upper()
                require(stem not in {"CON", "PRN", "AUX", "NUL", "CONIN$", "CONOUT$"}
                        and not re.fullmatch(r"(?:COM|LPT)[1-9¹²³]", stem), "reserved_archive_path")
            portable = info.filename.casefold()
            require(portable not in portable_names, "case_colliding_archive_paths")
            portable_names.add(portable)
            require(not info.flag_bits & 1, "encrypted_archive_not_supported")
            require(info.compress_type in {zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED},
                    "unsupported_archive_compression")
            require(not info.is_dir() and ((info.external_attr >> 16) & 0o170000) == 0o100000,
                    "non_regular_archive_entry")
            total += info.file_size
            require(info.file_size <= 5_000_000 and total <= 20_000_000, "expanded_archive_too_large")
        for name in portable_names:
            parts = name.split("/")
            require(not any("/".join(parts[:i]) in portable_names for i in range(1, len(parts))),
                    "archive_file_directory_collision")
        require(archive.testzip() is None, "archive_crc_failed")
        manifest = parse_json(archive.read(SKILL + "/PACKAGE_MANIFEST.json"))
        require(manifest.get("skill") == SKILL and isinstance(manifest.get("files"), dict), "invalid_package_manifest")
        expected_names = {SKILL + "/" + p for p in manifest["files"]} | {SKILL + "/PACKAGE_MANIFEST.json"}
        require(set(names) == expected_names, "archive_inventory_mismatch")
        for name, expected in manifest["files"].items():
            require(isinstance(expected, str) and re.fullmatch(r"[a-f0-9]{64}", expected), "invalid_package_digest")
            require(digest(archive.read(SKILL + "/" + name)) == expected, "package_file_changed")
        version = archive.read(SKILL + "/VERSION").decode("utf-8").strip()
        require(manifest.get("version") == version, "package_version_mismatch")
    return {"status": "VERIFIED", "sha256": digest(data), "version": version,
            "files_verified": len(manifest["files"]), "erp_validated": False}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--zip", required=True, type=Path)
    parser.add_argument("--compare", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        data = args.zip.read_bytes(); result = verify_archive(data)
        if args.compare:
            second = args.compare.read_bytes(); verify_archive(second)
            require(data == second, "cross_platform_package_mismatch")
            result["cross_platform_identical"] = True
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True); write_json(args.output, result)
        print(json.dumps(result, indent=2)); return 0
    except (Blocked, OSError, ValueError, KeyError, TypeError, zipfile.BadZipFile) as exc:
        print(json.dumps({"status": "BLOCKED", "reason": str(exc) if isinstance(exc, Blocked) else type(exc).__name__})); return 2


if __name__ == "__main__": raise SystemExit(main())
