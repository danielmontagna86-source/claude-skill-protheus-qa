"""Release consistency checks, independent of browser/TIR installation."""
from __future__ import annotations
import ast
import json
import re
from pathlib import Path
from tirqa_core import API, CONTRACT, TIR_COMMIT, TIR_VERSION


def validate(root: Path | None = None) -> list[str]:
    root = root or Path(__file__).resolve().parents[1]
    errors = []
    try:
        version = (root / "VERSION").read_text(encoding="utf-8").strip()
        if not re.fullmatch(r"\d+\.\d+\.\d+(?:-rc\.\d+)?", version): errors.append("Invalid version")
        plugin = json.loads((root / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
        marketplace = json.loads((root / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
        if plugin["version"] != version: errors.append("Plugin version drift")
        if marketplace["plugins"][0]["version"] != version: errors.append("Marketplace version drift")
        for path in ("CHANGELOG.md", "README.md"):
            if version not in (root / path).read_text(encoding="utf-8"): errors.append("Missing version: " + path)
        if not (root / f"RELEASE_NOTES/v{version}.md").is_file(): errors.append("Missing release notes")
        skill = (root / "SKILL.md").read_text(encoding="utf-8")
        headings = re.findall(r"^\|\s*\d+\s*\|\s*([^|]+?)\s*\|", skill, flags=re.M)
        if headings != CONTRACT: errors.append("Canonical 13-item contract changed")
        manifest = json.loads((root / "references/tir/public-api-manifest.json").read_text(encoding="utf-8"))
        if manifest["tir_version"] != TIR_VERSION or manifest["commit"] != TIR_COMMIT:
            errors.append("TIR baseline drift")
        for name, (required, allowed) in API.items():
            entry = manifest["methods"][name]
            if set(entry["required"]) != required or set(entry["allowed"]) != allowed:
                errors.append("API manifest drift: " + name)
        for path in (root / "scripts").glob("*.py"):
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for path in (root / "templates/tir").glob("*.json"):
            json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors.append(type(exc).__name__ + ": release inputs incomplete")
    return errors


if __name__ == "__main__":
    errors = validate()
    for message in errors: print(message)
    print("TIR release validation " + ("FAILED" if errors else "PASSED"))
    raise SystemExit(1 if errors else 0)
