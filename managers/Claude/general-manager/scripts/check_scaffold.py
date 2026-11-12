#!/usr/bin/env python3
"""Integrity check for this General Manager expert scaffold."""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME_RE = re.compile(r"(?:run |skill |follow \*\*|`)([a-z][a-z0-9-]{2,})(?:`|\*\*|\.md|\b)")
PATH_RE = re.compile(r"`([^`]+)`")
ESCAPED_HEADING_RE = re.compile(r"^\\#", re.MULTILINE)
BAD_PATTERNS = [
    (re.compile(r"workflowID-", re.I), "workflowID- typo"),
    (re.compile(r"folloWID-", re.I), "folloWID- typo"),
    (re.compile(r"inject-rules-on-action\.sh"), "retired shell rules hook"),
    (re.compile(r"work-items/.+/journal/"), "legacy work-item journal path"),
    (re.compile(r"(?<!/)facts/facts\.md"), "retired top-level facts/facts.md"),
]

RUNTIME_ALLOW = {
    ".claude/active-context.txt",
    ".claude/active-work-item.txt",
    ".claude/role-skills.md",
    "docs/role/role-definition.md",
}


def fail(findings: list[str], message: str) -> None:
    findings.append(message)


def load_known_tokens() -> set[str]:
    hook = ROOT / ".claude" / "hooks" / "inject_rules_on_action.py"
    spec = importlib.util.spec_from_file_location("inject_rules_on_action", hook)
    if spec is None or spec.loader is None:
        return set()
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return set(getattr(module, "KNOWN_TOKENS", []))


def skill_dirs() -> set[str]:
    base = ROOT / ".claude" / "skills"
    return {path.name for path in base.iterdir() if path.is_dir()} if base.is_dir() else set()


def named_skills(text: str) -> set[str]:
    known = skill_dirs()
    found = set()
    for match in SKILL_NAME_RE.finditer(text):
        name = match.group(1)
        if name in known or (ROOT / ".claude" / "skills" / name).exists():
            found.add(name)
    return found


def expand_path(raw: str) -> list[Path]:
    cleaned = raw.strip().rstrip("/")
    if not cleaned or cleaned.startswith("http"):
        return []
    if any(token in cleaned for token in ("<", ">", "*", "?")):
        pattern = cleaned
        for token in ("<id>", "<WID>", "<work-item-id>", "<node>", "<node-id>", "<change-id>", "<label>", "<task-id>"):
            pattern = pattern.replace(token, "*")
        pattern = re.sub(r"<[^>]+>", "*", pattern)
        return list(ROOT.glob(pattern))
    return [ROOT / cleaned]


def main() -> int:
    findings: list[str] = []
    skills = skill_dirs()
    docs = []
    for path in [ROOT / "CLAUDE.md", ROOT / "MyRole.txt", ROOT / "QUICK-START.md"]:
        if path.is_file():
            docs.append(path)
    docs.extend((ROOT / ".claude" / "skills").rglob("SKILL.md"))
    docs.extend((ROOT / ".claude" / "workflows").glob("*.md"))
    docs.append(ROOT / "facts" / "MEMORY-INDEX.md")

    for path in docs:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(ROOT).as_posix()
        for name in named_skills(text):
            if name not in skills:
                fail(findings, f"{rel}: missing skill folder `{name}`")
        if ESCAPED_HEADING_RE.search(text):
            fail(findings, f"{rel}: escaped markdown heading")
        for pattern, label in BAD_PATTERNS:
            if pattern.search(text) and rel != "EXPERT-REPAIR-PLAN.md":
                fail(findings, f"{rel}: {label}")
        for raw in PATH_RE.findall(text):
            if raw in RUNTIME_ALLOW:
                continue
            if raw.startswith(("facts/facts-", "facts/rules-", ".claude/skills/", "journals/", "work-items/", "docs/", "scripts/", "qa-sessions/")):
                matches = expand_path(raw)
                if not matches and "<" not in raw:
                    candidate = ROOT / raw
                    if not candidate.exists():
                        # Allow paths that are clearly work-item runtime artifacts.
                        if any(part in raw for part in ("<id>", "WID-", "nodes/", "agent-notes/")):
                            continue
                        fail(findings, f"{rel}: missing path `{raw}`")

    registry = ROOT / ".claude" / "workflows" / "workflow-registry.json"
    if registry.is_file():
        data = json.loads(registry.read_text(encoding="utf-8"))
        raw_workflows = data.get("workflows", data)
        if isinstance(raw_workflows, dict):
            entries = list(raw_workflows.values())
        elif isinstance(raw_workflows, list):
            entries = raw_workflows
        else:
            entries = []
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            instruction = entry.get("instruction_file")
            if not instruction:
                continue
            primary = ROOT / str(instruction)
            alt = ROOT / ".claude" / "workflows" / Path(str(instruction)).name
            if not primary.is_file() and not alt.is_file():
                fail(findings, f"workflow-registry: missing instruction_file `{instruction}`")

    known = load_known_tokens()
    vocab_sources = [
        ROOT / "facts" / "MEMORY-INDEX.md",
        ROOT / ".claude" / "skills" / "remember" / "SKILL.md",
        ROOT / ".claude" / "skills" / "promote-facts-rules" / "SKILL.md",
    ]
    token_re = re.compile(
        r"\b(?:decision:log|status:update|stakeholder:update|escalation:open|"
        r"cadence:review|write:doc|config:change|write:sql|sql:generate|"
        r"pr:open|git:push|git:commit)\b"
    )
    for path in vocab_sources:
        if not path.is_file():
            continue
        for token in token_re.findall(path.read_text(encoding="utf-8")):
            if token not in known:
                fail(findings, f"{path.relative_to(ROOT).as_posix()}: trigger `{token}` not in KNOWN_TOKENS")

    if findings:
        print("Scaffold check failed:")
        for item in findings:
            print(f"  - {item}")
        return 1
    print("Scaffold check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
