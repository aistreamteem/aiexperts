#!/usr/bin/env python3
"""Integrity check for this role expert scaffold. Exit non-zero on findings."""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALLOW_MISSING = {
    ".cursor/role-skills.md",
    ".cursor/plans/",
    "work-items/<id>/",
    "journals/work-items/<id>/",
}

SKILL_NAME = re.compile(r"(?:run\s+|skill\s+|invoke\s+)?[`*]{0,2}([a-z][a-z0-9-]+)/?[`*]{0,2}")
BACKTICK_PATH = re.compile(r"`([^`]+)`")
PLACEHOLDER = re.compile(r"<[^>]+>")
ESCAPED_HEADING = re.compile(r"(?m)^\\#")
BAD_PATTERNS = [
    re.compile(r"(?i)[a-z]wid-"),
    re.compile(r"2027-"),
    re.compile(r"(?<!work-items/)facts/facts\.md"),
    re.compile(r"-operations\.md"),
]


def _skills_on_disk() -> set[str]:
    skills = ROOT / ".cursor" / "skills"
    if not skills.is_dir():
        return set()
    return {p.name for p in skills.iterdir() if p.is_dir()}


def _named_skills(text: str) -> set[str]:
    # Conservative: only names that look like skill folders already on disk or
    # hyphenated phase names referenced as skills.
    found: set[str] = set()
    for match in re.finditer(
        r"\*\*([a-z][a-z0-9-]+)\*\*|`([a-z][a-z0-9-]+)`|run ([a-z][a-z0-9-]+)",
        text,
    ):
        name = next(g for g in match.groups() if g)
        if name in {
            "continue",
            "remember",
            "journal-keeper",
            "workflow-selector",
            "switch-context",
            "define-role",
            "promote-facts-rules",
            "integrate-docs",
            "memory-optimize",
            "operator-qa",
            "visual-page",
            "spec-parser",
            "implement-feature",
            "iterative-feature",
            "refactor",
            "scaffold-project",
            "diagram-generator",
            "hld-writer",
            "dd-writer",
            "task-breakdown",
            "git-workflow",
        }:
            found.add(name)
    return found


def _load_known_tokens() -> set[str]:
    hook = ROOT / ".cursor" / "hooks" / "inject_rules_on_action.py"
    spec = importlib.util.spec_from_file_location("inject_rules_on_action", hook)
    if spec is None or spec.loader is None:
        return set()
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    tokens = getattr(module, "KNOWN_TOKENS", [])
    return set(tokens) | {"none"}


def main() -> int:
    findings: list[str] = []
    on_disk = _skills_on_disk()
    scan_files = [
        ROOT / "AGENTS.md",
        ROOT / "MyRole.txt",
        ROOT / "README.md",
        ROOT / "QUICK-START.md",
        *sorted((ROOT / ".cursor" / "skills").glob("*/SKILL.md")),
        *sorted((ROOT / ".cursor" / "workflows").glob("*.md")),
    ]
    named: set[str] = set()
    for path in scan_files:
        if path.is_file():
            named |= _named_skills(path.read_text(encoding="utf-8", errors="replace"))
    # This role does not ship developer phase skills; do not require them.
    developer_only = {"hld-writer", "dd-writer", "task-breakdown", "git-workflow"}
    for skill in sorted(named - on_disk - developer_only):
        findings.append(f"missing skill folder: {skill}")

    registry = ROOT / ".cursor" / "workflows" / "workflow-registry.json"
    if registry.is_file():
        data = json.loads(registry.read_text(encoding="utf-8"))
        for key, entry in (data.get("workflows") or {}).items():
            rel = str((entry or {}).get("instruction_file") or "")
            if rel and not (ROOT / rel).is_file():
                findings.append(f"registry instruction missing: {key} -> {rel}")

    known = _load_known_tokens()
    trigger_line = re.compile(
        r"\*\*Triggers:\*\*\s*((?:`?none`?|`?write:doc`?|`?write:csv`?|`?write:sql`?|"
        r"`?sql:generate`?|`?pr:open`?|`?git:push`?|`?git:commit`?|`?config:change`?"
        r"|[,|\s])+)"
    )
    for path in [
        *sorted((ROOT / ".cursor" / "skills").glob("*/SKILL.md")),
        ROOT / "facts" / "MEMORY-INDEX.md",
    ]:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for match in trigger_line.finditer(text):
            for tok in re.split(r"[,\s|]+", match.group(1)):
                tok = tok.strip().strip("`.")
                if not tok:
                    continue
                if tok not in known:
                    findings.append(f"unknown trigger `{tok}` in {path.relative_to(ROOT)}")

    for path in ROOT.rglob("*.md"):
        if "visual-page" in path.parts and "runtime" in path.parts:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if ESCAPED_HEADING.search(text):
            findings.append(f"escaped heading in {path.relative_to(ROOT)}")
        if path.name in {"TRIGGER-INDEX.md"}:
            continue
        rel = str(path.relative_to(ROOT)).replace("\\", "/")
        for m in re.finditer(r"facts/facts\.md", text):
            start = m.start()
            prefix = text[max(0, start - 40) : start]
            if "work-items/" in prefix or prefix.endswith("./"):
                continue
            findings.append(f"stale top-level facts/facts.md in {rel}")
            break
        if re.search(r"(?i)[a-z]wid-", text):
            findings.append(f"stale workflowID typo in {rel}")
        if "2027-" in text:
            findings.append(f"future 2027- date in {rel}")
        if "-operations.md" in text:
            findings.append(f"stale -operations.md in {rel}")

    readme = ROOT / "README.md"
    quick = ROOT / "QUICK-START.md"
    if readme.is_file() and quick.is_file():
        if readme.read_text(encoding="utf-8") != quick.read_text(encoding="utf-8"):
            findings.append("README.md and QUICK-START.md differ")

    if findings:
        print("check_scaffold FAILED:")
        for item in findings:
            print(f"  - {item}")
        return 1
    print("check_scaffold OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
