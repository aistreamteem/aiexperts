#!/usr/bin/env python3
"""Integrity check for this pest-control-office Claude expert scaffold.

Exits non-zero on any finding. Standard library only.
"""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_SKILLS = {
    "define-role",
    "continue",
    "journal-keeper",
    "workflow-selector",
    "switch-context",
    "remember",
    "promote-facts-rules",
    "integrate-docs",
    "operator-qa",
    "memory-optimize",
}

# Runtime / relative paths that are created during a job or are not repo roots.
ALLOW_PATH_SUFFIXES = {
    "in/",
    "out/",
    "work/",
    "evidence/",
    "nodes/work-item.md",
    ".../rules.md",
    ".claude/active-work-item.txt",
    ".claude/active-qa-session.txt",
    "qa-sessions/Q*/",
    "whiteboard/scene.json",
    "whiteboard/edits.json",
    "whiteboard/server.json",
    "docs/design/hld.md",
    "docs/design/dd.md",
    "docs/design/requirements-summary.md",
    "docs/diagrams/",
    "docs/diagrams/index.html",
    "docs/decisions/",
    "docs/incident/assessment.md",
}

BAD_PATTERNS = [
    (re.compile(r"(?i)(?<![./\\])(?<![A-Za-z])[a-z]wid-"), "stale '…wid-' splice"),
    (re.compile(r"\b2027-"), "future placeholder year 2027"),
    (re.compile(r"(?m)^\\#"), "escaped markdown heading"),
    (re.compile(r"(?<!\./)(?<!work-items/<id>/)(?<!work-items/\{id\}/)(?<!/)facts/facts\.md"), "legacy top-level facts/facts.md"),
    (re.compile(r"(?<!\./)(?<!work-items/<id>/)(?<!work-items/\{id\}/)(?<!/)facts/rules\.md"), "legacy top-level facts/rules.md"),
    (re.compile(r"\bconfig:change\b"), "retired config:change trigger"),
    (re.compile(r"inject-rules-on-action\.sh"), "retired shell rules hook name"),
    (re.compile(r"workflowID-"), "stale workflowID- splice"),
]


def err(msg: str, findings: list[str]) -> None:
    findings.append(msg)


def load_known_tokens() -> list[str]:
    hook = ROOT / ".claude" / "hooks" / "inject_rules_on_action.py"
    spec = importlib.util.spec_from_file_location("rules_hook", hook)
    if spec is None or spec.loader is None:
        return []
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    tokens = getattr(mod, "KNOWN_TOKENS", [])
    return list(tokens) if isinstance(tokens, list) else []


def skill_dirs() -> set[str]:
    base = ROOT / ".claude" / "skills"
    if not base.is_dir():
        return set()
    return {p.name for p in base.iterdir() if p.is_dir()}


def check_named_skills(findings: list[str]) -> None:
    present = skill_dirs()
    for name in sorted(REQUIRED_SKILLS):
        if name not in present:
            err(f"missing required skill folder: .claude/skills/{name}/", findings)
    agents = (ROOT / "CLAUDE.md").read_text(encoding="utf-8")
    for name in ("hld-writer", "dd-writer", "task-breakdown", "git-workflow"):
        if re.search(rf"\b{name}\b", agents) and name not in present:
            err(f"CLAUDE.md names missing skill: {name}", findings)


def path_allowed(raw: str) -> bool:
    text = raw.strip().replace("\\", "/")
    if not text or " " in text or text.startswith(("http", "/health")):
        return True
    if text in {"/health"}:
        return True
    if text in ALLOW_PATH_SUFFIXES or text.rstrip("/") + "/" in ALLOW_PATH_SUFFIXES:
        return True
    if any(text.endswith(s) or text == s.rstrip("/") for s in ALLOW_PATH_SUFFIXES):
        return True
    if text.startswith(("root_path=", "journal_path=", "map_path=")):
        return True
    if "<" in text or ">" in text or "*" in text:
        return True
    candidate = ROOT / text
    if candidate.exists():
        return True
    # Relative work-item artifact mention without work-items/ prefix
    if text in {"in", "out", "work", "evidence"}:
        return True
    return False


def check_backticked_paths(findings: list[str]) -> None:
    files = [ROOT / "CLAUDE.md", ROOT / "MyRole.txt", ROOT / "README.md", ROOT / "QUICK-START.md"]
    files.extend((ROOT / ".claude" / "skills").glob("*/SKILL.md"))
    files.extend((ROOT / ".claude" / "workflows").glob("*.md"))
    path_re = re.compile(r"`([^`]+)`")
    for path in files:
        if not path.is_file():
            continue
        for match in path_re.findall(path.read_text(encoding="utf-8")):
            if "/" not in match and "\\" not in match:
                continue
            if not path_allowed(match):
                err(f"missing path in {path.relative_to(ROOT)}: `{match}`", findings)


def check_registry(findings: list[str]) -> None:
    reg = ROOT / ".claude" / "workflows" / "workflow-registry.json"
    data = json.loads(reg.read_text(encoding="utf-8"))
    workflows = data.get("workflows") if isinstance(data, dict) else None
    if not isinstance(workflows, dict):
        err("workflow-registry.json has no workflows object", findings)
        return
    for key, meta in workflows.items():
        if not isinstance(meta, dict):
            continue
        instruction = meta.get("instruction_file")
        if isinstance(instruction, str) and not (ROOT / instruction).is_file():
            err(f"registry workflow {key}: missing {instruction}", findings)


def check_triggers(findings: list[str]) -> None:
    known = set(load_known_tokens()) | {"none"}
    if not (known - {"none"}):
        err("KNOWN_TOKENS missing from inject_rules_on_action.py", findings)
    token_re = re.compile(r"\b(write:[\w-]+|sql:[\w-]+|git:[\w-]+|pr:[\w-]+|config:[\w-]+)\b")
    texts = []
    for skill in (ROOT / ".claude" / "skills").glob("*/SKILL.md"):
        texts.append((str(skill.relative_to(ROOT)), skill.read_text(encoding="utf-8")))
    idx = ROOT / "facts" / "MEMORY-INDEX.md"
    if idx.is_file():
        texts.append(("facts/MEMORY-INDEX.md", idx.read_text(encoding="utf-8")))
    for label, text in texts:
        for tok in token_re.findall(text):
            if tok not in known:
                err(f"unknown trigger token `{tok}` in {label}", findings)


def check_bad_patterns(findings: list[str]) -> None:
    skip_names = {"check_scaffold.py", "TRIGGER-INDEX.md", "trigger-index.json"}
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.name in skip_names:
            continue
        if path.suffix.lower() not in {".md", ".py", ".txt", ".json"}:
            continue
        if "__pycache__" in path.parts:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        rel = path.relative_to(ROOT).as_posix()
        for pattern, label in BAD_PATTERNS:
            for match in pattern.finditer(text):
                window = text[max(0, match.start() - 48) : match.start()]
                if "legacy" in label and "work-items/" in window:
                    continue
                if "legacy" in label and "its `" in window and "facts/" in match.group(0):
                    # already rewritten to work-items/<id>/facts/...
                    continue
                err(f"{label} in {rel}", findings)
                break


def check_readme_pair(findings: list[str]) -> None:
    readme = ROOT / "README.md"
    quick = ROOT / "QUICK-START.md"
    if readme.is_file() and quick.is_file():
        if readme.read_bytes() != quick.read_bytes():
            err("README.md and QUICK-START.md differ", findings)


def main() -> int:
    findings: list[str] = []
    check_named_skills(findings)
    check_registry(findings)
    check_triggers(findings)
    check_bad_patterns(findings)
    check_readme_pair(findings)
    check_backticked_paths(findings)
    if findings:
        print(f"check_scaffold: {len(findings)} finding(s)")
        for item in findings:
            print(f" - {item}")
        return 1
    print("check_scaffold: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
