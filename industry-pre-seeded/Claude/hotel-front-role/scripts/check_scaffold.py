#!/usr/bin/env python3
"""Integrity checks for this Cursor expert scaffold. Exit non-zero on findings."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Skills this hotel-role expert actually uses (DESIGN + MyRole + AGENTS).
CANONICAL_SKILLS = {
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
    "visual-page",
}

ALLOW_MISSING_PATHS = {
    ".claude/role-skills.md",
    ".claude/active-work-item.txt",  # legacy read-only
    ".claude/active-qa-session.txt",
    ".claude/plans/",
}

HEADER_ESCAPE = re.compile(r"^\\#", re.MULTILINE)
SKILL_NAME = re.compile(r"(?:run\s+)?`?([a-z][a-z0-9-]+)`?(?:\s+skill)?", re.I)
BACKTICK_PATH = re.compile(r"`([^`]+)`")


def _fail(findings: list[str], msg: str) -> None:
    findings.append(msg)


def check_canonical_skills(findings: list[str]) -> None:
    skills_root = ROOT / ".claude" / "skills"
    for name in sorted(CANONICAL_SKILLS):
        if not (skills_root / name / "SKILL.md").is_file():
            _fail(findings, f"missing canonical skill folder: {name}")


def check_registry(findings: list[str]) -> None:
    reg = ROOT / ".claude" / "workflows" / "workflow-registry.json"
    if not reg.is_file():
        _fail(findings, "missing workflow-registry.json")
        return
    try:
        data = json.loads(reg.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        _fail(findings, f"workflow-registry.json invalid: {exc}")
        return
    raw = data.get("workflows") if isinstance(data, dict) else None
    entries: list[dict] = []
    if isinstance(raw, dict):
        for wid, meta in raw.items():
            if isinstance(meta, dict):
                entries.append({"id": wid, **meta})
            else:
                entries.append({"id": wid})
    elif isinstance(raw, list):
        entries = [e for e in raw if isinstance(e, dict)]
    else:
        _fail(findings, "workflow-registry.json: no workflows map/list")
        return
    for entry in entries:
        instr = entry.get("instruction_file") or entry.get("file")
        wid = entry.get("id") or entry.get("name")
        if not instr:
            if wid:
                candidate = ROOT / ".claude" / "workflows" / f"{wid}.md"
                if not candidate.is_file():
                    _fail(findings, f"workflow file missing for {wid}")
            continue
        path = ROOT / str(instr).replace("\\", "/")
        if not path.is_file():
            _fail(findings, f"instruction_file missing: {instr}")


def check_known_tokens(findings: list[str]) -> None:
    hook = ROOT / ".claude" / "hooks" / "inject_rules_on_action.py"
    if not hook.is_file():
        _fail(findings, "missing inject_rules_on_action.py")
        return
    ns: dict = {}
    try:
        exec(hook.read_text(encoding="utf-8"), ns)
    except Exception as exc:  # noqa: BLE001
        _fail(findings, f"cannot load KNOWN_TOKENS: {exc}")
        return
    known = set(ns.get("KNOWN_TOKENS") or [])
    vocab_files = [
        ROOT / ".claude" / "skills" / "remember" / "SKILL.md",
        ROOT / ".claude" / "skills" / "promote-facts-rules" / "SKILL.md",
        ROOT / "facts" / "MEMORY-INDEX.md",
    ]
    token_re = re.compile(r"\b(write:[a-z]+|git:[a-z]+|pr:[a-z]+|sql:[a-z]+|config:[a-z]+)\b")
    for path in vocab_files:
        if not path.is_file():
            continue
        for tok in token_re.findall(path.read_text(encoding="utf-8")):
            if tok != "none" and tok not in known:
                _fail(findings, f"{path.relative_to(ROOT)} mentions unknown trigger `{tok}`")


def check_escaped_headers(findings: list[str]) -> None:
    for path in ROOT.rglob("*.md"):
        if "node_modules" in path.parts:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if HEADER_ESCAPE.search(text):
            _fail(findings, f"escaped heading in {path.relative_to(ROOT)}")


def check_bad_patterns(findings: list[str]) -> None:
    for path in ROOT.rglob("*"):
        if path.suffix.lower() not in {".md", ".txt", ".py", ".json"}:
            continue
        if path.name == "check_scaffold.py":
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if re.search(r"(?i)workflowID-|folloWID-|newID-workflow", text):
            _fail(findings, f"stale ID-insertion typo in {path.relative_to(ROOT)}")
        if "2027-" in text:
            _fail(findings, f"future 2027- date in {path.relative_to(ROOT)}")


def check_readme_pair(findings: list[str]) -> None:
    readme = ROOT / "README.md"
    quick = ROOT / "QUICK-START.md"
    if readme.is_file() and quick.is_file():
        if readme.read_text(encoding="utf-8") != quick.read_text(encoding="utf-8"):
            # Hotel role docs differ slightly by design in some seeds; warn only if both claim to be copies
            r = readme.read_text(encoding="utf-8")
            q = quick.read_text(encoding="utf-8")
            if abs(len(r) - len(q)) < 50 and r[:80] == q[:80]:
                _fail(findings, "README.md and QUICK-START.md drifted")


def main() -> int:
    findings: list[str] = []
    check_canonical_skills(findings)
    check_registry(findings)
    check_known_tokens(findings)
    check_escaped_headers(findings)
    check_bad_patterns(findings)
    check_readme_pair(findings)
    if findings:
        print("check_scaffold FAILED:")
        for item in findings:
            print(f"  - {item}")
        return 1
    print("check_scaffold OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
