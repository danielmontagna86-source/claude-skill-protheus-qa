#!/usr/bin/env python3
"""Validate the Claude Skill package structure.

This script intentionally uses only Python standard library modules so it can run
locally, in CI, or in restricted build environments without extra dependencies.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

SKILL_NAME = "testing-protheus-routines"
MAX_DESCRIPTION_LENGTH = 1024
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

REQUIRED_DIRECTORIES = [
    "references",
    "routines",
    "templates",
    "examples",
    "evals",
]

REQUIRED_FILES = [
    "SKILL.md",
    "README.md",
    "INSTALL.md",
    "USAGE.md",
    "evals/eval-mvp.md",
    "routines/INDEX.md",
    "routines/FINA080.md",
]

REQUIRED_RESPONSE_SECTIONS = [
    "Objetivo do teste",
    "Base funcional/TDN usada",
    "Tipo de customização",
    "Risco QA",
    "Técnica recomendada",
    "Cenários positivos",
    "Cenários negativos",
    "Cenários de regressão",
    "Massa de dados",
    "Tabelas/campos",
    "Exemplo de automação ou roteiro",
    "Evidência esperada",
    "Limitações",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_frontmatter(skill_md: str) -> dict[str, str]:
    if not skill_md.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter delimiter '---'.")

    parts = skill_md.split("---", 2)
    if len(parts) < 3:
        raise ValueError("SKILL.md must contain opening and closing YAML frontmatter delimiters.")

    frontmatter_text = parts[1].strip()
    frontmatter: dict[str, str] = {}

    for raw_line in frontmatter_text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"Invalid frontmatter line: {raw_line!r}")
        key, value = line.split(":", 1)
        frontmatter[key.strip()] = value.strip().strip('"').strip("'")

    return frontmatter


def validate() -> tuple[list[str], list[str]]:
    root = repo_root()
    errors: list[str] = []
    warnings: list[str] = []

    for directory in REQUIRED_DIRECTORIES:
        if not (root / directory).is_dir():
            errors.append(f"Missing required directory: {directory}")

    for file_path in REQUIRED_FILES:
        if not (root / file_path).is_file():
            errors.append(f"Missing required file: {file_path}")

    skill_file = root / "SKILL.md"
    if skill_file.is_file():
        try:
            skill_md = read_text(skill_file)
            frontmatter = parse_frontmatter(skill_md)
        except Exception as exc:  # noqa: BLE001 - validation should report any parsing issue
            errors.append(str(exc))
        else:
            name = frontmatter.get("name", "")
            description = frontmatter.get("description", "")

            if name != SKILL_NAME:
                errors.append(f"Invalid skill name: expected {SKILL_NAME!r}, found {name!r}")

            if not NAME_PATTERN.fullmatch(name):
                errors.append("Skill name must use only lowercase letters, numbers, and hyphens.")

            if not description:
                errors.append("Frontmatter description is required.")
            elif len(description) > MAX_DESCRIPTION_LENGTH:
                errors.append(
                    f"Description is too long: {len(description)} chars; "
                    f"maximum is {MAX_DESCRIPTION_LENGTH}."
                )

            for section in REQUIRED_RESPONSE_SECTIONS:
                if section not in skill_md:
                    errors.append(f"SKILL.md is missing required response section: {section}")

            if "Regra anti-alucinação" not in skill_md:
                errors.append("SKILL.md must include the anti-hallucination rule.")

    index_file = root / "routines" / "INDEX.md"
    if index_file.is_file():
        index_md = read_text(index_file)
        for routine in ["FINA050", "FINA080", "MATA010", "MATA120", "MATA220", "MATA410", "MATA460"]:
            if routine not in index_md:
                errors.append(f"routines/INDEX.md is missing routine: {routine}")

    eval_file = root / "evals" / "eval-mvp.md"
    if eval_file.is_file():
        eval_md = read_text(eval_file)
        for expected in ["Eval 1 - FINA050", "Eval 2 - MATA410", "Falhas que indicam problema"]:
            if expected not in eval_md:
                errors.append(f"evals/eval-mvp.md is missing expected section: {expected}")

    if root.name != SKILL_NAME:
        warnings.append(
            f"Repository folder is {root.name!r}; package/install folder must be {SKILL_NAME!r}. "
            "This is expected when developing from the GitHub repository, but the final ZIP must use the skill name."
        )

    return errors, warnings


def main() -> int:
    errors, warnings = validate()

    for warning in warnings:
        print(f"WARNING: {warning}", file=sys.stderr)

    if errors:
        print("Skill validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("Skill validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
