#!/usr/bin/env python3
"""Integrity check for this expert scaffold. Exit non-zero on any finding."""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Paths created at runtime or intentionally optional
ALLOW_PATHS = {
    ".cursor/active-context.txt",
    ".cursor/active-work-item.txt",
    ".cursor/role-skills.md",
    "work-items/<id>/",
    "journals/work-items/<id>/",
}

SKILL_NAME_RE = re.compile(
    r"\b(continue|journal-keeper|workflow-selector|switch-context|remember|"
    r"promote-facts-rules|integrate-docs|memory-optimize|operator-qa|define-role|"
    r"spec-parser|implement-feature|iterative-feature|refactor|scaffold-project|"
    r"diagram-generator|visual-page|hld-writer|dd-writer|task-breakdown|git-workflow)\b"
)
BACKTICK_PATH_RE = re.compile(r"`([^`]+)`")
PLACEHOLDER_RE = re.compile(r"<[^>]+>|WID-[A-Z0-9]+|YYYY-MM-DD")
ESCAPED_HEADING_RE = re.compile(r"^\\#", re.MULTILINE)
BAD_PATTERNS = [
    (re.compile(r"[a-z]wid-", re.I), "stale 'wid-' splice (e.g. workflowID-)"),
    (re.compile(r"2027-"), "future seed date 2027-"),
    (re.compile(r"(?<!work-items/<id>/)facts/facts\.md"), "top-level facts/facts.md"),
    (re.compile(r"-operations\.md"), None),  # allowed for this role
]


def _err(findings: list[str], msg: str) -> None:
    findings.append(msg)


def _load_known_tokens() -> list[str]:
    hook = ROOT / ".cursor" / "hooks" / "inject_rules_on_action.py"
    spec = importlib.util.spec_from_file_location("inject_rules_on_action", hook)
    if spec is None or spec.loader is None:
        return []
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    tokens = getattr(mod, "KNOWN_TOKENS", [])
    return list(tokens) if isinstance(tokens, list) else []


def _skill_dirs() -> set[str]:
    skills = ROOT / ".cursor" / "skills"
    if not skills.is_dir():
        return set()
    return {p.name for p in skills.iterdir() if p.is_dir()}


def check_named_skills(findings: list[str]) -> None:
    present = _skill_dirs()
    required_role = {
        "continue",
        "journal-keeper",
        "workflow-selector",
        "switch-context",
        "remember",
        "promote-facts-rules",
        "integrate-docs",
        "memory-optimize",
        "operator-qa",
        "define-role",
    }
    # Developer phase skills must NOT be required for this role
    for name in required_role:
        if name not in present:
            _err(findings, f"missing required skill folder: .cursor/skills/{name}/")
    # If AGENTS/MyRole name a skill that has no folder, flag it — except known N/A developer phases
    skip = {"hld-writer", "dd-writer", "task-breakdown", "git-workflow", "spec-parser", "implement-feature", "iterative-feature", "refactor", "scaffold-project", "diagram-generator"}
    texts = []
    for rel in ("AGENTS.md", "MyRole.txt", "README.md"):
        path = ROOT / rel
        if path.is_file():
            texts.append(path.read_text(encoding="utf-8"))
    for skill_dir in (ROOT / ".cursor" / "skills").glob("*/SKILL.md"):
        texts.append(skill_dir.read_text(encoding="utf-8"))
    for wf in (ROOT / ".cursor" / "workflows").glob("*.md"):
        texts.append(wf.read_text(encoding="utf-8"))
    blob = "\n".join(texts)
    for match in SKILL_NAME_RE.finditer(blob):
        name = match.group(1)
        if name in skip:
            continue
        if name not in present:
            _err(findings, f"named skill has no folder: {name}")


def check_registry(findings: list[str]) -> None:
    reg = ROOT / ".cursor" / "workflows" / "workflow-registry.json"
    if not reg.is_file():
        _err(findings, "missing workflow-registry.json")
        return
    try:
        data = json.loads(reg.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        _err(findings, f"invalid workflow-registry.json: {exc}")
        return
    workflows = data.get("workflows") if isinstance(data, dict) else None
    if isinstance(workflows, dict):
        items = workflows.values()
    elif isinstance(workflows, list):
        items = workflows
    elif isinstance(data, dict):
        items = [v for v in data.values() if isinstance(v, dict) and "instruction_file" in v]
    else:
        items = []
    for item in items:
        if not isinstance(item, dict):
            continue
        instr = item.get("instruction_file") or item.get("file")
        if not instr:
            continue
        path = ROOT / str(instr).replace("\\", "/")
        if not path.is_file():
            _err(findings, f"registry instruction_file missing: {instr}")


def check_triggers(findings: list[str]) -> None:
    known = set(_load_known_tokens())
    if not known:
        _err(findings, "KNOWN_TOKENS missing from inject_rules_on_action.py")
        return
    vocab_files = [
        ROOT / ".cursor" / "skills" / "remember" / "SKILL.md",
        ROOT / ".cursor" / "skills" / "promote-facts-rules" / "SKILL.md",
        ROOT / "facts" / "MEMORY-INDEX.md",
    ]
    token_re = re.compile(r"\b(write:[a-z]+|sql:generate|pr:open|git:push|git:commit|config:change)\b")
    for path in vocab_files:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for tok in token_re.findall(text):
            if tok not in known and tok != "none":
                _err(findings, f"trigger token `{tok}` in {path.relative_to(ROOT)} not in KNOWN_TOKENS")


def check_escaped_and_patterns(findings: list[str]) -> None:
    for path in ROOT.rglob("*.md"):
        if "node_modules" in path.parts:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            continue
        if ESCAPED_HEADING_RE.search(text):
            _err(findings, f"escaped heading in {path.relative_to(ROOT)}")
        rel = str(path.relative_to(ROOT)).replace("\\", "/")
        # Skip generated trigger index for pattern noise
        if rel.endswith("TRIGGER-INDEX.md"):
            continue
        if re.search(r"[a-z]wid-", text, re.I):
            _err(findings, f"stale wid- splice in {rel}")
        if "2027-" in text:
            _err(findings, f"future date 2027- in {rel}")


def check_readme_pair(findings: list[str]) -> None:
    readme = ROOT / "README.md"
    quick = ROOT / "QUICK-START.md"
    if readme.is_file() and quick.is_file():
        if readme.read_text(encoding="utf-8") != quick.read_text(encoding="utf-8"):
            _err(findings, "README.md and QUICK-START.md differ")


def main() -> int:
    findings: list[str] = []
    check_named_skills(findings)
    check_registry(findings)
    check_triggers(findings)
    check_escaped_and_patterns(findings)
    check_readme_pair(findings)
    # Hook entry points
    for name in (
        "inject_journal_context.py",
        "inject_rules_on_action.py",
        "on_stop.py",
        "merge_agent_notes.py",
        "journal_snapshot.py",
        "journal_fields.py",
    ):
        if not (ROOT / ".cursor" / "hooks" / name).is_file():
            _err(findings, f"missing hook {name}")
    if findings:
        print("check_scaffold FAILED:")
        for item in findings:
            print(f"  - {item}")
        return 1
    print("check_scaffold OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
