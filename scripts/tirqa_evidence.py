"""Strict, local evidence validation. Integrity is not cryptographic authenticity."""
from __future__ import annotations
import struct
import zlib
from pathlib import Path
from tirqa_core import (ASSERTIONS, bundle_files, bundle_manifest, digest,
                        is_link, load_json, require, text)

MAX_FILE_BYTES = 25_000_000
MAX_FILES = 5000


def regular_files(root: Path):
    require(root.is_dir() and not is_link(root), "regular_directory_required")
    pending, count = [root], 0
    while pending:
        directory = pending.pop()
        for path in sorted(directory.iterdir()):
            count += 1
            require(count <= MAX_FILES, "too_many_evidence_entries")
            require(not is_link(path), "link_in_evidence")
            if path.is_dir():
                pending.append(path)
            else:
                require(path.is_file(), "non_regular_evidence")
                require(path.stat().st_size <= MAX_FILE_BYTES, "evidence_file_too_large")
                yield path


def _scanline_layout(width: int, height: int, channels: int, depth: int,
                     interlace: int) -> list[tuple[int, int]]:
    passes = ((0, 0, 1, 1),) if interlace == 0 else (
        (0, 0, 8, 8), (4, 0, 8, 8), (0, 4, 4, 8), (2, 0, 4, 4),
        (0, 2, 2, 4), (1, 0, 2, 2), (0, 1, 1, 2))
    rows = []
    for x, y, dx, dy in passes:
        columns = max(0, (width - x + dx - 1) // dx)
        count = max(0, (height - y + dy - 1) // dy)
        if columns and count:
            rows.append((1 + (columns * channels * depth + 7) // 8, count))
    return rows


def _valid_scanlines(compressed: bytes, layout: list[tuple[int, int]]) -> bool:
    expected = sum(stride * count for stride, count in layout)
    # Bounded decoding; the compressed/file size alone cannot prevent a PNG bomb.
    if not (0 < expected <= 128 * 1024 * 1024):
        return False
    try:
        decoder = zlib.decompressobj()
        raw = decoder.decompress(compressed, expected + 1)
        if (len(raw) != expected or not decoder.eof or decoder.unused_data
                or decoder.unconsumed_tail):
            return False
    except zlib.error:
        return False
    offset = 0
    for stride, count in layout:
        for _ in range(count):
            if raw[offset] > 4:
                return False
            offset += stride
    return True


def png_is_structurally_valid(data: bytes) -> bool:
    """Validate CRC, PNG layout and bounded pixel stream, not visual authenticity."""
    if not data.startswith(b"\x89PNG\r\n\x1a\n") or len(data) > MAX_FILE_BYTES:
        return False
    pos, chunks = 8, 0
    compressed = bytearray()
    idat_started, idat_ended, palette = False, False, False
    layout, color, depth = [], -1, 0
    formats = {0: (1, {1, 2, 4, 8, 16}), 2: (3, {8, 16}),
               3: (1, {1, 2, 4, 8}), 4: (2, {8, 16}), 6: (4, {8, 16})}
    while pos + 12 <= len(data):
        size = struct.unpack(">I", data[pos:pos+4])[0]
        end = pos + 12 + size
        if end > len(data) or chunks >= 10000:
            return False
        kind, payload = data[pos+4:pos+8], data[pos+8:pos+8+size]
        if not all(65 <= c <= 90 or 97 <= c <= 122 for c in kind) or kind[2] & 32:
            return False
        crc = struct.unpack(">I", data[pos+8+size:end])[0]
        if (zlib.crc32(kind + payload) & 0xffffffff) != crc:
            return False
        if chunks == 0:
            if kind != b"IHDR" or size != 13:
                return False
            width, height, depth, color, compression, filtering, interlace = struct.unpack(">IIBBBBB", payload)
            if (not (0 < width <= 30000 and 0 < height <= 30000) or color not in formats
                    or depth not in formats[color][1] or compression != 0 or filtering != 0
                    or interlace not in (0, 1)):
                return False
            layout = _scanline_layout(width, height, formats[color][0], depth, interlace)
        elif kind == b"IHDR":
            return False
        elif kind == b"PLTE":
            if (palette or idat_started or color in (0, 4) or size == 0 or size % 3
                    or size > 768 or (color == 3 and size // 3 > 2**depth)):
                return False
            palette = True
        elif kind == b"IDAT":
            if idat_ended or (color == 3 and not palette):
                return False
            idat_started = True
            compressed.extend(payload)
        elif kind == b"IEND":
            return (size == 0 and end == len(data) and idat_started
                    and _valid_scanlines(bytes(compressed), layout))
        else:
            if not kind[0] & 32:  # Unknown critical chunk cannot be ignored.
                return False
            if idat_started:
                idat_ended = True
        pos, chunks = end, chunks + 1
    return False


def screenshots(root: Path) -> list[Path]:
    if not root.exists():
        return []
    result = []
    for path in regular_files(root):
        if path.suffix.lower() == ".png":
            require(png_is_structurally_valid(path.read_bytes()), "invalid_png_evidence")
            result.append(path)
    return result


def artifact_hashes(root: Path) -> dict:
    files = {}
    for path in regular_files(root):
        rel = path.relative_to(root)
        require(".private" not in rel.parts, "private_files_in_evidence")
        # Only our own top-level manifest is excluded. No basename-wide exemptions.
        if rel.as_posix() != "evidence-manifest.json":
            files[rel.as_posix()] = digest(path.read_bytes())
    return dict(sorted(files.items()))


def validate_success(result: dict, root: Path) -> None:
    require(type(result.get("schema_version")) is int and result["schema_version"] == 1,
            "invalid_result_schema")
    require(text(result.get("run_id")), "run_id_required")
    counts = result.get("counts", {})
    require(isinstance(counts, dict)
            and counts.keys() == {"tests", "failures", "errors", "skipped"}
            and all(type(v) is int for v in counts.values())
            and counts == {"tests": 1, "failures": 0, "errors": 0, "skipped": 0},
            "invalid_pass_evidence")
    require(type(result.get("exit_code")) is int and result["exit_code"] == 0
            and result.get("private_cleanup") == "REMOVED"
            and result.get("evidence_status") == "LOCAL_ONLY", "invalid_pass_finalization")
    for key in ("checks_expected", "checks_passed", "screenshots"):
        require(type(result.get(key)) is int and result[key] > 0, "invalid_pass_evidence")
    require(result["checks_expected"] == result["checks_passed"]
            and result.get("cleanup") == "SESSION_CLOSED", "invalid_pass_evidence")
    require(result.get("execution_mode") in {"live", "simulated"}
            and type(result.get("erp_validated")) is bool, "execution_mode_required")
    require(result["erp_validated"] is (result["execution_mode"] == "live"),
            "simulation_cannot_validate_erp")
    identity = result.get("identity", [])
    require(isinstance(identity, list) and len(identity) == 4
            and all(isinstance(x, dict) and x.get("observed") is True for x in identity)
            and {x.get("kind") for x in identity} == {"environment", "group", "branch", "routine"},
            "invalid_pass_identity")
    require(len(screenshots(root / "screenshots")) == result["screenshots"], "screenshot_inventory_mismatch")
    case, profile = load_json(root / "case.json"), load_json(root / "profile.json")
    expected_manifest = bundle_manifest(bundle_files(case, profile))
    require(result.get("case_id") == case["case_id"]
            and result.get("bundle_sha256") == expected_manifest["bundle_sha256"], "result_input_mismatch")
    steps, observations = case["steps"], result.get("observations")
    require(isinstance(observations, list) and len(observations) == len(steps), "observations_incomplete")
    require(sum(s["method"] in ASSERTIONS for s in steps) == result["checks_expected"],
            "assertion_count_mismatch")
    for index, (step, actual) in enumerate(zip(steps, observations), start=1):
        require(isinstance(actual, dict) and type(actual.get("step")) is int
                and actual["step"] == index and actual.get("method") == step["method"]
                and actual.get("source_id") == step["source_id"] and actual.get("status") == "PASS",
                "observation_contract_mismatch")
        if step["method"] in ASSERTIONS:
            expected = step["kwargs"]["user_value"] if step["method"] == "CheckResult" else step["expected"]
            require(type(actual.get("expected")) is type(expected) and actual["expected"] == expected
                    and type(actual.get("observed")) is type(expected) and actual["observed"] == expected,
                    "observation_value_mismatch")
