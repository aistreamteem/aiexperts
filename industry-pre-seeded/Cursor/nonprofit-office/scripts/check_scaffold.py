#!/usr/bin/env python3
"""Integrity check for the nonprofit-office Cursor expert scaffold.

Exits non-zero on any finding. Stdlib only.
"""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Leftover developer skills kept in the folder but unused by this role.
LEFTOVER_DEV_SKILLS = {
    "spec-parser",
    "implement-feature",
    "iterative-feature",
    "refactor",
    "scaffold-project",
    "diagram-generator",
}

ALLOW_MISSING = {
    ".cursor/role-skills.md",
    ".cursor/active-work-item.txt",
    ".cursor/active-qa-session.txt",
}

REQUIRED_SKILLS = {
    "continue",
    "define-role",
    "journal-keeper",
    "remember",
    "workflow-selector",
    "operator-qa",
    "promote-facts-rules",
    "switch-context",
    "integrate-docs",
    "memory-optimize",
}

PLACEHOLDER = re.compile(r"<[^>]+>")
ESCAPED_HEADING = re.compile(r"^\\#", re.M)
BAD_PATTERNS = [
    (re.compile(r"(?i)workflowID-|WorkflowID-|newID-workflow|folloWID-"), "workflowID- style typo"),
    (re.compile(r"2027-"), "future dated 2027- leftover"),
    (re.compile(r"facts-operations\.md|rules-operations\.md"), "operations memory should be shared"),
    (re.compile(r"inject-rules-on-action\.sh"), "shell rules hook name leftover"),
]
TRIGGER_TOKEN = re.compile(r"\b(write:[a-z]+|sql:[a-z]+|git:[a-z]+|pr:[a-z]+|config:[a-z]+)\b")
BACKTICK_PATH = re.compile(r"`([^`]+)`")


def _load_known_tokens() -> set[str]:
    hook = ROOT / ".cursor" / "hooks" / "inject_rules_on_action.py"
    if not hook.is_file():
        return set()
    spec = importlib.util.spec_from_file_location("inject_rules_on_action", hook)
    if spec is None or spec.loader is None:
        return set()
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    tokens = getattr(module, "KNOWN_TOKENS", [])
    return set(tokens) if isinstance(tokens, list) else set()


def _skills() -> set[str]:
    base = ROOT / ".cursor" / "skills"
    if not base.is_dir():
        return set()
    return {p.name for p in base.iterdir() if p.is_dir()}


def _path_ok(raw: str) -> bool:
    path = raw.strip().replace("\\", "/")
    if not path or " " in path or path.startswith("http"):
        return True
    if path in ALLOW_MISSING:
        return True
    if PLACEHOLDER.search(path):
        return True
    if path.endswith("/"):
        return (ROOT / path).exists() or True
    interesting = path.startswith(
        ("docs/", "facts/", ".cursor/", "journals/", "scripts/", "work-items/", "qa-sessions/")
    ) or path in {"MyRole.txt", "AGENTS.md", "README.md", "QUICK-START.md"}
    if not interesting:
        return True
    return (ROOT / path).exists()


def main() -> int:
    findings: list[str] = []
    skills = _skills()
    known = _load_known_tokens()

    for name in REQUIRED_SKILLS:
        if name not in skills:
            findings.append(f"required role skill missing: {name}")

    for name in ("facts-shared.md", "rules-shared.md", "MEMORY-INDEX.md"):
        if not (ROOT / "facts" / name).is_file():
            findings.append(f"missing facts/{name}")

    for name in (
        "inject_journal_context.py",
        "inject_rules_on_action.py",
        "journal_fields.py",
        "merge_agent_notes.py",
        "journal_snapshot.py",
        "on_stop.py",
    ):
        if not (ROOT / ".cursor" / "hooks" / name).is_file():
            findings.append(f"missing hook .cursor/hooks/{name}")

    registry = ROOT / ".cursor" / "workflows" / "workflow-registry.json"
    if not registry.is_file():
        findings.append("missing workflow-registry.json")
    else:
        try:
            data = json.loads(registry.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            findings.append("workflow-registry.json: invalid JSON")
            data = {}
        workflows = data.get("workflows") if isinstance(data, dict) else None
        entries: list[dict] = []
        if isinstance(workflows, dict):
            entries = [v for v in workflows.values() if isinstance(v, dict)]
        elif isinstance(workflows, list):
            entries = [v for v in workflows if isinstance(v, dict)]
        for entry in entries:
            instr = entry.get("instruction_file") or entry.get("file")
            if isinstance(instr, str) and instr.strip():
                path = ROOT / instr.replace("\\", "/")
                alt = ROOT / ".cursor" / "workflows" / Path(instr).name
                if not path.is_file() and not alt.is_file():
                    findings.append(f"registry instruction missing: {instr}")

    scan_files: list[Path] = []
    for name in ("AGENTS.md", "MyRole.txt", "QUICK-START.md", "README.md"):
        p = ROOT / name
        if p.is_file():
            scan_files.append(p)
    for p in (ROOT / ".cursor" / "skills").rglob("SKILL.md"):
        if p.parent.name in LEFTOVER_DEV_SKILLS:
            continue  # unused leftover skills; do not invent their design docs
        scan_files.append(p)
    scan_files.extend((ROOT / ".cursor" / "workflows").glob("*.md"))
    for name in ("MEMORY-INDEX.md", "HOW-MEMORY-LOADING-WORKS.md"):
        p = ROOT / "facts" / name
        if p.is_file():
            scan_files.append(p)

    for path in scan_files:
        text = path.read_text(encoding="utf-8")
        rel = str(path.relative_to(ROOT)).replace("\\", "/")
        if ESCAPED_HEADING.search(text):
            findings.append(f"{rel}: escaped heading \\#")
        for pattern, label in BAD_PATTERNS:
            if pattern.search(text):
                findings.append(f"{rel}: {label}")
        if "Triggers" in text or "trigger" in text.lower():
            for token in TRIGGER_TOKEN.findall(text):
                if known and token not in known:
                    findings.append(f"{rel}: trigger token `{token}` not in KNOWN_TOKENS")
        for raw in BACKTICK_PATH.findall(text):
            if "/" in raw or raw.endswith((".md", ".py", ".json", ".txt", ".mdc", ".sh")):
                if not _path_ok(raw):
                    findings.append(f"{rel}: missing path `{raw}`")

    readme = ROOT / "README.md"
    quick = ROOT / "QUICK-START.md"
    if readme.is_file() and quick.is_file():
        rtext = readme.read_text(encoding="utf-8")
        qtext = quick.read_text(encoding="utf-8")
        if rtext != qtext and "QUICK-START.md" not in rtext:
            findings.append("README.md and QUICK-START.md differ (and README is not a pointer)")

    if findings:
        print("Scaffold check FAILED:")
        for item in findings:
            print(f" - {item}")
        return 1
    print("Scaffold check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
