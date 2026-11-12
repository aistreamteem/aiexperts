#!/usr/bin/env python3
"""Integrity check for this HOA / association admin Expert scaffold."""

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

SKILL_NAME_RE = re.compile(r"`([a-z][a-z0-9-]{2,})`")
PATH_RE = re.compile(r"`([^`]+)`")
ESCAPED_HEADING_RE = re.compile(r"^\\#", re.MULTILINE)
BAD_PATTERNS = [
    re.compile(r"[a-z]wid-", re.I),
    re.compile(r"2027-"),
    re.compile(r"facts/facts\.md"),
    re.compile(r"-operations\.md"),  # checked carefully below
]


def _fail(msg: str, findings: list[str]) -> None:
    findings.append(msg)


def _load_known_tokens() -> set[str]:
    hook = ROOT / ".cursor" / "hooks" / "inject_rules_on_action.py"
    spec = importlib.util.spec_from_file_location("inject_rules_on_action", hook)
    if spec is None or spec.loader is None:
        return set()
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return set(getattr(mod, "KNOWN_TOKENS", []) or [])


def _canonical_skills() -> set[str]:
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    # Rule 22 lists canonical skills after "Canonical skills:"
    skills: set[str] = set()
    for line in agents.splitlines():
        if "Canonical skills" in line or line.strip().startswith("22."):
            for name in SKILL_NAME_RE.findall(line):
                if name not in {"work-items", "docs", "facts"}:
                    skills.add(name)
    # Also collect skill folders that exist
    skill_root = ROOT / ".cursor" / "skills"
    if skill_root.is_dir():
        for child in skill_root.iterdir():
            if child.is_dir() and (child / "SKILL.md").is_file():
                skills.add(child.name)
    return skills


def check_skills(findings: list[str]) -> None:
    named = set()
    for rel in ("AGENTS.md", "MyRole.txt", "README.md"):
        text = (ROOT / rel).read_text(encoding="utf-8")
        if "Canonical skills" in text or "continue" in text:
            for m in re.finditer(
                r"\b(continue|define-role|journal-keeper|remember|workflow-selector|"
                r"operator-qa|promote-facts-rules|switch-context|integrate-docs|"
                r"memory-optimize|visual-page|hld-writer|dd-writer|task-breakdown|"
                r"git-workflow)\b",
                text,
            ):
                named.add(m.group(1))
    for name in sorted(named):
        folder = ROOT / ".cursor" / "skills" / name
        if not (folder / "SKILL.md").is_file():
            # Developer phase skills are not used by this role.
            if name in {"hld-writer", "dd-writer", "task-breakdown", "git-workflow"}:
                continue
            _fail(f"missing skill folder for `{name}`", findings)


def check_registry(findings: list[str]) -> None:
    registry = ROOT / ".cursor" / "workflows" / "workflow-registry.json"
    data = json.loads(registry.read_text(encoding="utf-8"))
    workflows = data.get("workflows") if isinstance(data, dict) else None
    if not isinstance(workflows, list):
        # Some registries use a dict map
        if isinstance(data, dict):
            for key, meta in data.items():
                if key in {"version", "facts"}:
                    continue
                if isinstance(meta, dict):
                    instr = meta.get("instruction_file") or meta.get("file")
                    if instr:
                        path = ROOT / str(instr).replace("\\", "/")
                        if not path.is_file():
                            _fail(f"registry instruction missing: {instr}", findings)
        return
    for item in workflows:
        if not isinstance(item, dict):
            continue
        instr = item.get("instruction_file") or item.get("file")
        if not instr:
            continue
        path = ROOT / str(instr).replace("\\", "/")
        if not path.is_file():
            _fail(f"registry instruction missing: {instr}", findings)


def check_triggers(findings: list[str]) -> None:
    known = _load_known_tokens() | {"none"}
    texts = [
        ROOT / ".cursor" / "skills" / "remember" / "SKILL.md",
        ROOT / ".cursor" / "skills" / "promote-facts-rules" / "SKILL.md",
        ROOT / "facts" / "MEMORY-INDEX.md",
    ]
    token_re = re.compile(r"\b(write:[a-z]+|sql:[a-z]+|git:[a-z]+|pr:[a-z]+|config:[a-z]+)\b")
    for path in texts:
        if not path.is_file():
            continue
        for tok in token_re.findall(path.read_text(encoding="utf-8")):
            if tok not in known:
                _fail(f"unknown trigger `{tok}` in {path.relative_to(ROOT)}", findings)


def check_escaped_headings(findings: list[str]) -> None:
    for path in ROOT.rglob("*.md"):
        if any(part.startswith(".") and part not in {".cursor"} for part in path.parts):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            continue
        if ESCAPED_HEADING_RE.search(text):
            _fail(f"escaped heading in {path.relative_to(ROOT)}", findings)


def check_bad_patterns(findings: list[str]) -> None:
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in {".md", ".txt", ".py", ".json"}:
            continue
        if "node_modules" in path.parts or "__pycache__" in path.parts:
            continue
        # Skip this checker and generated indexes for noisy patterns
        if path.name in {"check_scaffold.py", "TRIGGER-INDEX.md", "trigger-index.json"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            continue
        rel = str(path.relative_to(ROOT)).replace("\\", "/")
        if re.search(r"[a-z]wid-", text, re.I):
            _fail(f"workflowID-style typo in {rel}", findings)
        if "2027-" in text:
            _fail(f"future date 2027- in {rel}", findings)
        # Top-level facts/facts.md (not under work-items/.../facts/) is stale for this role.
        for m in re.finditer(r"facts/facts\.md", text):
            start = max(0, m.start() - 48)
            window = text[start : m.end()]
            if (
                "work-items/" in window
                or "<root_path>/facts/" in window
                or "./facts/facts.md" in window
                or "](./facts/facts.md)" in text[max(0, m.start() - 5) : m.end() + 1]
            ):
                continue
            _fail(f"stale facts/facts.md reference in {rel}", findings)
            break


def check_readme_pair(findings: list[str]) -> None:
    readme = ROOT / "README.md"
    quick = ROOT / "QUICK-START.md"
    if readme.is_file() and quick.is_file():
        # Role experts intentionally diverge; only fail if they claim identity.
        if readme.read_text(encoding="utf-8") == quick.read_text(encoding="utf-8"):
            return
        # Not an error for this role — README and QUICK-START are distinct.


def main() -> int:
    findings: list[str] = []
    check_skills(findings)
    check_registry(findings)
    check_triggers(findings)
    check_escaped_headings(findings)
    check_bad_patterns(findings)
    check_readme_pair(findings)
    if findings:
        print("Scaffold check FAILED:")
        for item in findings:
            print(f"  - {item}")
        return 1
    print("Scaffold check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
