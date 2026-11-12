#!/usr/bin/env python3
"""Integrity check for the school-office-admin Cursor expert scaffold."""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKTICK_PATH = re.compile(r"`([^`]+)`")
ESCAPED_HEADING = re.compile(r"^\\#", re.M)
ROLE_SKILLS = {
    "define-role",
    "continue",
    "journal-keeper",
    "remember",
    "promote-facts-rules",
    "workflow-selector",
    "switch-context",
    "operator-qa",
    "integrate-docs",
    "memory-optimize",
    "visual-page",
}
# Leftover scaffold skills still present; do not invent their developer artifacts.
SKIP_PATH_CHECK_SKILLS = {
    "diagram-generator",
    "implement-feature",
    "iterative-feature",
    "refactor",
    "scaffold-project",
    "spec-parser",
}
RUNTIME_ALLOW = {
    ".cursor/active-work-item.txt",
    ".cursor/active-qa-session.txt",
    ".cursor/role-skills.md",
}
BAD_LINE_PATTERNS = [
    (re.compile(r"[a-z]wid-", re.I), "stale workflowID/wid splice"),
    (re.compile(r"2027-"), "future archive date 2027-"),
    (re.compile(r"(?<![\w/-])facts/facts\.md"), "top-level facts/facts.md"),
    (re.compile(r"(?<![\w/-])facts/rules\.md"), "top-level facts/rules.md"),
    (re.compile(r"-operations\.md"), "retired operations memory filename"),
    (re.compile(r"workflowID-", re.I), "workflowID- typo"),
    (re.compile(r"folloWID", re.I), "folloWID typo"),
]


def load_known_tokens() -> set[str]:
    hook = ROOT / ".cursor" / "hooks" / "inject_rules_on_action.py"
    spec = importlib.util.spec_from_file_location("inject_rules_on_action", hook)
    if spec is None or spec.loader is None:
        return set()
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return set(getattr(module, "KNOWN_TOKENS", []))


def skill_dirs() -> set[str]:
    base = ROOT / ".cursor" / "skills"
    return {p.name for p in base.iterdir() if p.is_dir()} if base.is_dir() else set()


def should_check_path(raw: str) -> bool:
    cleaned = raw.strip().rstrip(".,;")
    if not cleaned or cleaned in RUNTIME_ALLOW:
        return False
    if any(ch in cleaned for ch in "<>* \n\t"):
        return False
    if cleaned.startswith("http"):
        return False
    return cleaned.startswith(
        (
            ".cursor/",
            "facts/",
            "journals/",
            "work-items/",
            "docs/",
            "scripts/",
            "qa-sessions/",
        )
    ) or cleaned in {"AGENTS.md", "MyRole.txt", "README.md", "QUICK-START.md", "DESIGN.md"}


def main() -> int:
    errors: list[str] = []
    skills = skill_dirs()
    known_tokens = load_known_tokens()

    # 1. Role-required skills named in AGENTS/MyRole exist.
    for path in (ROOT / "AGENTS.md", ROOT / "MyRole.txt"):
        text = path.read_text(encoding="utf-8")
        for name in ROLE_SKILLS:
            if name in text and name not in skills:
                errors.append(f"{path.name}: missing skill folder `.cursor/skills/{name}/`")

    scan_files = [
        ROOT / "AGENTS.md",
        ROOT / "MyRole.txt",
        ROOT / "README.md",
        ROOT / "QUICK-START.md",
        ROOT / "DESIGN.md",
        *sorted((ROOT / ".cursor" / "skills").glob("*/SKILL.md")),
        *sorted((ROOT / ".cursor" / "workflows").glob("*.md")),
        ROOT / "facts" / "MEMORY-INDEX.md",
        ROOT / "facts" / "HOW-MEMORY-LOADING-WORKS.md",
    ]

    for path in scan_files:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(ROOT).as_posix()
        skill_name = path.parent.name if path.name == "SKILL.md" else ""
        skip_paths = skill_name in SKIP_PATH_CHECK_SKILLS

        if ESCAPED_HEADING.search(text):
            errors.append(f"{rel}: escaped markdown heading \\#")

        for pat, label in BAD_LINE_PATTERNS:
            for i, line in enumerate(text.splitlines(), 1):
                if pat.search(line):
                    # Work-item relative facts.md mentions are fine.
                    if "facts/facts.md" in line and "work-items/" in line:
                        continue
                    if "facts/rules.md" in line and "work-items/" in line:
                        continue
                    errors.append(f"{rel}:{i}: {label}")

        if not skip_paths:
            for match in BACKTICK_PATH.finditer(text):
                raw = match.group(1)
                if not should_check_path(raw):
                    continue
                candidate = ROOT / raw.replace("\\", "/")
                if not candidate.exists():
                    errors.append(f"{rel}: missing path `{raw}`")

        for match in re.finditer(r"\*\*Triggers:\*\*\s*([^\n]+)", text):
            for tok in re.split(r"[,\s|/]+", match.group(1).strip()):
                tok = tok.strip().strip("`")
                if not tok or tok in {"none", "..."}:
                    continue
                if tok.startswith(("write:", "git:", "sql:", "pr:", "config:")) and known_tokens:
                    if tok not in known_tokens:
                        errors.append(f"{rel}: unknown trigger token `{tok}`")

    registry = ROOT / ".cursor" / "workflows" / "workflow-registry.json"
    if registry.is_file():
        data = json.loads(registry.read_text(encoding="utf-8"))
        workflows = data.get("workflows", {}) if isinstance(data, dict) else {}
        entries: list[dict] = []
        if isinstance(workflows, dict):
            entries = [v for v in workflows.values() if isinstance(v, dict)]
        elif isinstance(workflows, list):
            entries = [v for v in workflows if isinstance(v, dict)]
        for entry in entries:
            instr = entry.get("instruction_file") or entry.get("file")
            if isinstance(instr, str) and instr.strip():
                path = ROOT / instr.replace("\\", "/")
                if not path.is_file():
                    errors.append(f"workflow-registry: missing instruction_file `{instr}`")

    readme = ROOT / "README.md"
    quick = ROOT / "QUICK-START.md"
    if readme.is_file() and quick.is_file():
        r = readme.read_text(encoding="utf-8").strip()
        q = quick.read_text(encoding="utf-8").strip()
        if r != q and "QUICK-START.md" not in r and "README.md" not in q:
            errors.append("README.md and QUICK-START.md differ and neither points at the other")

    if errors:
        print("check_scaffold FAILED:")
        for err in sorted(set(errors)):
            print(" -", err)
        return 1
    print("check_scaffold OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
