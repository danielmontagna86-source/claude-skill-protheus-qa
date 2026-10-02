"""Offline contracts for TIR 2.14.10. Standard library only; never imports TIR."""
from __future__ import annotations

import ast
import hashlib
import importlib.metadata
import json
import math
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

ENGINE_FILES = ("tirqa_core.py", "tirqa_evidence.py", "tirqa_runner.py")
TIR_VERSION = "2.14.10"
TIR_COMMIT = "dbc12e7a0563174a3f6c16832046229d71d464cf"
# Deliberately supported PUBLIC subset, not the whole TIR API.
API = {
    "SearchBrowse": ({"term"}, {"term", "key", "identifier", "index", "column"}),
    "SetButton": ({"button"}, {"button", "sub_item", "position", "is_browse"}),
    "ClickFolder": ({"item"}, {"item", "position"}),
    "WaitShow": ({"string"}, {"string", "timeout", "match_case"}),
    "WaitHide": ({"string"}, {"string", "timeout", "match_case"}),
    "GetValue": ({"field"}, {"field", "grid", "line", "grid_number", "position"}),
    "IfExists": ({"string"}, {"string", "timeout"}),
    "CheckResult": ({"field", "user_value"},
                    {"field", "user_value", "grid", "line", "grid_number"}),
    "LoadGrid": (set(), set()),
}
ASSERTIONS = {"GetValue", "IfExists", "CheckResult"}
NAVIGATION_BUTTONS = {"Visualizar", "Fechar", "Voltar", "Cancelar", "Consultar",
                      "View", "Close", "Back", "Cancel"}
SECRET_KEYS = {"password", "passwordcfg", "dbpassword", "user", "usercfg",
               "dbuser", "token", "api_key", "apikey", "secret"}
CONFIG_KEYS = {"Url", "Environment", "Browser", "Language", "POUILogin",
               "NewHome", "SSOLogin", "TimeOut", "Headless"}
CONTRACT = ["Objetivo do teste", "Base funcional/TDN usada", "Tipo de customização",
            "Risco QA", "Técnica recomendada", "Cenários positivos", "Cenários negativos",
            "Cenários de regressão", "Massa de dados", "Tabelas/campos",
            "Exemplo de automação ou roteiro", "Evidência esperada", "Limitações"]


class Blocked(ValueError):
    """A contract or safety requirement prevents further processing."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise Blocked(message)


def _pairs(pairs: list) -> dict:
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate_json_key")
        result[key] = value
    return result


def is_link(path: Path) -> bool:
    return path.is_symlink() or bool(getattr(path, "is_junction", lambda: False)())


def parse_json(raw: bytes) -> dict:
    require(len(raw) <= 2_000_000, "json_too_large")
    try:
        data = json.loads(raw.decode("utf-8"), object_pairs_hook=_pairs,
                          parse_constant=lambda _: (_ for _ in ()).throw(Blocked("nonfinite_json")))
    except RecursionError:
        raise Blocked("json_too_deep") from None
    require(isinstance(data, dict), "json_object_required")
    pending, nodes = [(data, 0)], 0
    while pending:
        item, depth = pending.pop(); nodes += 1
        require(depth <= 64 and nodes <= 100000, "json_too_deep_or_complex")
        if isinstance(item, dict): pending.extend((v, depth + 1) for v in item.values())
        elif isinstance(item, list): pending.extend((v, depth + 1) for v in item)
        elif isinstance(item, float):
            require(math.isfinite(item), "nonfinite_json")
    return data


def load_json(path: Path) -> dict:
    require(not is_link(path) and path.is_file(), "regular_file_required")
    require(path.stat().st_size <= 2_000_000, "json_too_large")
    return parse_json(path.read_bytes())


def encoded(data: object) -> bytes:
    return (json.dumps(data, ensure_ascii=False, sort_keys=True, indent=2,
                       allow_nan=False) + "\n").encode("utf-8")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_json(path: Path, data: object) -> None:
    # Exclusive creation: evidence and approved inputs are never overwritten.
    with path.open("xb") as stream:
        stream.write(encoded(data))


def text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip()) and len(value) <= 10_000


def check_secrets(value: object) -> None:
    if isinstance(value, dict):
        require(not any(k.lower() in SECRET_KEYS for k in value), "secret_in_input")
        for item in value.values():
            check_secrets(item)
    elif isinstance(value, list):
        for item in value:
            check_secrets(item)


def exact_keys(data: dict, required: set, optional: set = frozenset()) -> None:
    require(isinstance(data, dict), "object_required")
    require(required <= data.keys(), "missing_required_keys")
    require(data.keys() <= required | optional, "unknown_keys")


def validate_profile(profile: dict, execution: bool = False) -> None:
    exact_keys(profile, {"schema_version", "enabled", "environment_kind", "tir_version",
                         "config", "setup", "identity_checks", "baseline"})
    require(type(profile["schema_version"]) is int and profile["schema_version"] == 1,
            "unsupported_schema")
    require(type(profile["enabled"]) is bool, "enabled_must_be_boolean")
    require(profile["environment_kind"] == "homologation", "homologation_only")
    require(profile["tir_version"] == TIR_VERSION, "wrong_tir_version")
    if execution:
        require(profile["enabled"], "execution_disabled")
    config = profile["config"]
    exact_keys(config, {"Url", "Environment", "Browser", "Language", "TimeOut"},
               CONFIG_KEYS - {"Url", "Environment", "Browser", "Language", "TimeOut"})
    require(all(text(config[k]) for k in ("Url", "Environment", "Browser", "Language")),
            "invalid_config_text")
    require(not any(ch.isspace() or ord(ch) < 32 or ord(ch) == 127 for ch in config["Url"]), "url_control_character")
    url = urlsplit(config["Url"])
    _ = url.port  # validate a malformed or out-of-range port before any process starts
    require(url.scheme == "https" and bool(url.hostname) and not url.username
            and not url.password and not url.query and not url.fragment, "unsafe_url")
    require(not url.hostname.endswith((".invalid", ".example")), "placeholder_url")
    require(config["Browser"] in {"Chrome", "Firefox"}, "unsupported_browser")
    require(type(config["TimeOut"]) is int and 1 <= config["TimeOut"] <= 300, "invalid_timeout")
    for key in ("POUILogin", "NewHome", "SSOLogin", "Headless"):
        require(key not in config or type(config[key]) is bool, "boolean_config_required")
    setup = profile["setup"]
    exact_keys(setup, {"initial_program", "date", "group", "branch", "module"})
    require(all(text(v) for v in setup.values()), "incomplete_setup")
    datetime.strptime(setup["date"], "%d/%m/%Y")
    checks = profile["identity_checks"]
    require(isinstance(checks, list) and len(checks) == 3, "three_identity_checks_required")
    kinds = set()
    for check in checks:
        exact_keys(check, {"kind", "text"})
        require(text(check["text"]), "empty_identity_check")
        require(isinstance(check["kind"], str), "identity_kind_must_be_text")
        kinds.add(check["kind"])
    require(kinds == {"environment", "group", "branch"}, "identity_scope_missing")
    require(len({check["text"] for check in checks}) == 3, "distinct_identity_markers_required")
    baseline = profile["baseline"]
    exact_keys(baseline, {"release", "appserver", "webapp", "lib", "rpo", "interface_evidence"})
    require(all(text(v) for v in baseline.values()), "baseline_incomplete")
    serialized = json.dumps(profile, ensure_ascii=False)
    require(not re.search(r"PREENCHER|CHANGE_ME|REPLACE_ME|<[^>]+>", serialized), "placeholder_profile")
    check_secrets(profile)


def validate_step(step: dict) -> None:
    exact_keys(step, {"method", "kwargs", "source_id"}, {"expected"})
    method, kwargs = step["method"], step["kwargs"]
    require(isinstance(method, str) and method in API, "unsupported_public_method")
    required, allowed = API[method]
    exact_keys(kwargs, required, allowed - required)
    require(text(step["source_id"]), "step_source_required")
    for key, value in kwargs.items():
        if key in {"grid", "index", "is_browse", "match_case"}:
            require(type(value) is bool, "boolean_argument_required")
        elif key in {"line", "grid_number", "position"}:
            minimum = 0 if method == "GetValue" and key == "position" else 1
            require(type(value) is int and minimum <= value <= 100_000, "invalid_position")
        elif key == "timeout":
            require(type(value) is int and 1 <= value <= 300, "invalid_step_timeout")
        elif key == "user_value":
            require(isinstance(value, (str, bool, int, float)) and value is not None,
                    "invalid_expected_value")
        elif key == "key" and kwargs.get("index") is True:
            require(type(value) is int and value >= 1, "invalid_browse_index")
        else:
            require(isinstance(value, str), "string_argument_required")
    if method in {"GetValue", "IfExists"}:
        require("expected" in step and step["expected"] is not None, "expected_required")
        require(type(step["expected"]) in {str, bool, int, float}, "scalar_expected_required")
        if method == "IfExists":
            require(type(step["expected"]) is bool, "boolean_expected_required")
    else:
        require("expected" not in step, "unexpected_expected_key")
    if method == "SetButton":
        require(kwargs["button"] in NAVIGATION_BUTTONS and not kwargs.get("sub_item"),
                "read_only_navigation_only")
    encoded(step)  # also rejects NaN and infinity supplied programmatically


def validate_case(case: dict) -> None:
    exact_keys(case, {"schema_version", "case_id", "title", "routine", "routine_marker",
                      "mode", "sources", "oracle", "fixture", "steps"})
    require(type(case["schema_version"]) is int and case["schema_version"] == 1, "unsupported_schema")
    require(isinstance(case["case_id"], str) and
            re.fullmatch(r"[A-Z][A-Z0-9_-]{1,63}", case["case_id"]), "invalid_case_id")
    require(all(text(case[k]) for k in ("title", "routine", "routine_marker")), "case_text_required")
    # Writes are deliberately NOT released until a real ERP pilot proves isolation/cleanup.
    require(case["mode"] == "read_only", "writes_not_released")
    sources = case["sources"]
    require(isinstance(sources, list) and 1 <= len(sources) <= 100, "sources_required")
    ids = set()
    for source in sources:
        exact_keys(source, {"id", "uri", "revision", "status"})
        require(all(text(v) for v in source.values()), "incomplete_source")
        require(source["status"] == "confirmed", "unconfirmed_source")
        require(source["id"] not in ids, "duplicate_source_id")
        ids.add(source["id"])
    exact_keys(case["oracle"], {"source_id", "description", "approved_by"})
    require(case["oracle"]["source_id"] in ids and
            all(text(v) for v in case["oracle"].values()), "independent_oracle_required")
    exact_keys(case["fixture"], {"synthetic", "description", "record_key"})
    require(case["fixture"]["synthetic"] is True and text(case["fixture"]["description"])
            and text(case["fixture"]["record_key"]), "synthetic_fixture_required")
    steps = case["steps"]
    require(isinstance(steps, list) and 1 <= len(steps) <= 200, "steps_required")
    for step in steps:
        validate_step(step)
        require(step["source_id"] in ids, "unknown_step_source")
    require(any(step["method"] in ASSERTIONS for step in steps), "business_assertion_required")
    require(not re.search(r"PREENCHER|CHANGE_ME|REPLACE_ME|<[^>]+>",
                          json.dumps(case, ensure_ascii=False)), "placeholder_case")
    check_secrets(case)


def render_test(case: dict, profile: dict) -> bytes:
    case = json.loads(encoded(case))
    profile = json.loads(encoded(profile))
    code = ('"""Generated review artifact. Execute via run_tir_suite.py, never directly."""\n'
            'from tirqa_runner import CaseTest\n\n'
            'class TestApprovedCase(CaseTest):\n'
            f'    case = {case!r}\n'
            f'    profile = {profile!r}\n')
    ast.parse(code)
    return code.encode("utf-8")


def bundle_files(case: dict, profile: dict) -> dict[str, bytes]:
    validate_case(case)
    validate_profile(profile)
    return {"case.json": encoded(case), "profile.json": encoded(profile),
            "test_case.py": render_test(case, profile)}


def bundle_manifest(files: dict[str, bytes]) -> dict:
    hashes = {name: digest(data) for name, data in sorted(files.items())}
    return {"schema_version": 1, "tir_version": TIR_VERSION, "tir_commit": TIR_COMMIT,
            "files": hashes, "bundle_sha256": digest(encoded(hashes))}


def generate(case: dict, profile: dict, destination: Path) -> dict:
    files = bundle_files(case, profile)
    root = Path(__file__).resolve().parents[1]
    require(not destination.resolve().is_relative_to(root), "workspace_must_be_outside_skill")
    require(not destination.exists(), "destination_exists")
    destination.mkdir(parents=True, mode=0o700)
    for name, data in files.items():
        with (destination / name).open("xb") as stream:
            stream.write(data)
    manifest = bundle_manifest(files)
    write_json(destination / "manifest.json", manifest)
    return manifest


def verify_bundle(directory: Path) -> tuple[dict, dict, dict]:
    require(not is_link(directory), "symlink_bundle")
    case, profile = load_json(directory / "case.json"), load_json(directory / "profile.json")
    expected = bundle_files(case, profile)
    for name, content in expected.items():
        path = directory / name
        require(not is_link(path) and path.is_file(), "bundle_file_missing")
        require(path.read_bytes() == content, "bundle_tampered")
    manifest = load_json(directory / "manifest.json")
    require(manifest == bundle_manifest(expected), "manifest_tampered")
    return case, profile, manifest


def engine_hash(directory: Path | None = None) -> str:
    root = directory or Path(__file__).resolve().parent
    return digest(encoded({name: digest((root / name).read_bytes()) for name in ENGINE_FILES}))


def preflight(profile: dict) -> dict:
    validate_profile(profile)
    try:
        installed = importlib.metadata.version("tir_framework")
    except importlib.metadata.PackageNotFoundError:
        installed = None
    checks = {"python_312": sys.version_info[:2] == (3, 12),
              "tir_exact": installed == TIR_VERSION, "execution_enabled": profile["enabled"]}
    return {"status": "READY_FOR_AUTHORIZATION" if all(checks.values()) else "BLOCKED",
            "checks": checks, "python": sys.version.split()[0], "tir_installed": installed,
            "network_checked": False, "browser_started": False, "erp_validated": False,
            "engine_sha256": engine_hash(),
            "dependency_security": "REVIEW_REQUIRED_NOT_A_CLEAN_AUDIT",
            "dependency_note": "The pinned TIR runtime includes requests 2.31.0 with known advisories."}


def approve(policy: dict, case: dict, profile: dict, manifest: dict,
            now: datetime | None = None) -> None:
    exact_keys(policy, {"schema_version", "environment_kind", "target", "approved_by",
                        "expires_at", "bundle_sha256", "engine_sha256", "allowed_buttons",
                        "integrations_blocked", "least_privilege_confirmed", "max_seconds", "dependency_risks_reviewed"})
    require(type(policy["schema_version"]) is int and policy["schema_version"] == 1, "unsupported_policy")
    require(policy["environment_kind"] == "homologation", "policy_not_homologation")
    target = {"Url": profile["config"]["Url"], "Environment": profile["config"]["Environment"],
              "group": profile["setup"]["group"], "branch": profile["setup"]["branch"]}
    require(policy["target"] == target, "target_mismatch")
    require(policy["bundle_sha256"] == manifest["bundle_sha256"], "unapproved_bundle")
    require(policy["engine_sha256"] == engine_hash(), "unapproved_engine")
    require(policy["dependency_risks_reviewed"] is True, "dependency_risk_review_required")
    require(text(policy["approved_by"]), "approver_required")
    require(text(policy["expires_at"]), "expiry_must_be_text")
    try:
        expiry = datetime.fromisoformat(policy["expires_at"].replace("Z", "+00:00"))
    except ValueError:
        raise Blocked("invalid_expiry_timestamp") from None
    require(expiry.tzinfo is not None, "timezone_required")
    current = now or datetime.now(timezone.utc)
    require(0 < (expiry - current).total_seconds() <= 86400, "approval_expired_or_too_long")
    require(policy["integrations_blocked"] is True and policy["least_privilege_confirmed"] is True,
            "environment_safety_not_confirmed")
    require(type(policy["max_seconds"]) is int and 1 <= policy["max_seconds"] <= 1800,
            "policy_timeout_invalid")
    require(isinstance(policy["allowed_buttons"], list)
            and all(text(x) for x in policy["allowed_buttons"]), "invalid_button_allowlist")
    for step in case["steps"]:
        if step["method"] == "SetButton":
            require(step["kwargs"]["button"] in policy["allowed_buttons"], "button_not_approved")
            require(not step["kwargs"].get("sub_item"), "submenu_not_released")
    check_secrets(policy)


def inspect_sources(paths: list[Path], encoding: str) -> list[dict]:
    require(encoding in {"utf-8", "utf-8-sig", "cp1252"}, "explicit_supported_encoding_required")
    result = []
    for path in paths:
        require(path.is_file() and not is_link(path), "regular_source_required")
        require(path.stat().st_size <= 10_000_000, "source_too_large")
        original = path.read_bytes()
        source = original.decode(encoding, errors="strict")
        symbols = re.findall(r"(?im)^\s*(?:user\s+|static\s+)?(?:function|class)\s+([\w.]+)", source)
        result.append({"file": path.name, "sha256": digest(original), "encoding": encoding,
                       "bytes": len(original), "symbols": sorted(set(symbols)),
                       "analysis": "lexical_only_not_advpl_parser", "modified": False})
    return result
