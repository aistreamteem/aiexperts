#!/usr/bin/env python3
"""Integrity check for this Cursor equipment-rental expert scaffold.

Exits non-zero on any finding. Standard library only.
"""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FINDINGS: list[str] = []

ALLOW_PATHS = {
    ".cursor/role-skills.md",
    ".cursor/active-work-item.txt",
    ".cursor/active-qa-session.txt",
    ".cursor/plans/",
    "work-items/<id>/",
    "journals/work-items/<id>/",
    "qa-sessions/Q*/",
}

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

SKILL_NAME_RE = re.compile(
    r"\*\*(continue|define-role|journal-keeper|remember|workflow-selector|"
    r"operator-qa|promote-facts-rules|switch-context|integrate-docs|"
    r"memory-optimize|visual-page|hld-writer|dd-writer|task-breakdown|"
    r"git-workflow|implement-feature|iterative-feature|spec-parser|"
    r"scaffold-project|diagram-generator|refactor)\*\*",
    re.I,
)
BACKTICK_PATH_RE = re.compile(r"`([^`]+)`")
PLACEHOLDER_RE = re.compile(r"<[^>]+>|\bWID\b|\*")
ESCAPED_HEADING_RE = re.compile(r"^\\#", re.M)
STALE_PATTERNS = [
    (re.compile(r"(?i)[a-z]wid-"), "stale '…wid-' insertion (e.g. workflowID-)"),
    (re.compile(r"2027-"), "future archive date 2027-"),
    (re.compile(r"(?<!work-items/<id>/)(?<!work-items/<work-item-id>/)`facts/facts\.md`"), "top-level facts/facts.md reference"),
    (re.compile(r"facts-developer\.md|rules-developer\.md|facts-incident|rules-incident"), "developer/incident memory leftover"),
    (re.compile(r"inject-rules-on-action\.sh"), "legacy rules hook .sh name"),
    (re.compile(r"config:change"), "retired config:change trigger"),
]


def note(msg: str) -> None:
    FINDINGS.append(msg)


def load_known_tokens() -> set[str]:
    hook = ROOT / ".cursor" / "hooks" / "inject_rules_on_action.py"
    spec = importlib.util.spec_from_file_location("inject_rules_on_action", hook)
    if spec is None or spec.loader is None:
        note("cannot load inject_rules_on_action.py for KNOWN_TOKENS")
        return set()
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    tokens = getattr(module, "KNOWN_TOKENS", [])
    return set(tokens) if isinstance(tokens, list) else set()


def check_canonical_skills() -> None:
    for name in sorted(CANONICAL_SKILLS):
        folder = ROOT / ".cursor" / "skills" / name / "SKILL.md"
        if not folder.is_file():
            note(f"missing canonical skill folder: .cursor/skills/{name}/")


def check_named_skills() -> None:
    texts = []
    for rel in ("AGENTS.md", "MyRole.txt", "README.md", "QUICK-START.md"):
        path = ROOT / rel
        if path.is_file():
            texts.append(path.read_text(encoding="utf-8"))
    for skill_dir in (ROOT / ".cursor" / "skills").glob("*/SKILL.md"):
        texts.append(skill_dir.read_text(encoding="utf-8"))
    for wf in (ROOT / ".cursor" / "workflows").glob("*.md"):
        texts.append(wf.read_text(encoding="utf-8"))
    named: set[str] = set()
    for text in texts:
        for match in SKILL_NAME_RE.finditer(text):
            named.add(match.group(1).lower())
    # Developer pipeline skill names may still appear in kept leftover folders;
    # only require folders for names that are canonical OR that have a folder already expected.
    for name in sorted(named):
        if name in {"hld-writer", "dd-writer", "task-breakdown", "git-workflow"}:
            # Not used by this rental role; mention is a finding if required by AGENTS/MyRole.
            agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
            myrole = (ROOT / "MyRole.txt").read_text(encoding="utf-8")
            if name in agents.lower() or name in myrole.lower():
                note(f"AGENTS/MyRole names unused developer skill `{name}`")
            continue
        folder = ROOT / ".cursor" / "skills" / name / "SKILL.md"
        if not folder.is_file() and name in CANONICAL_SKILLS:
            note(f"named skill missing folder: {name}")


def path_exists(raw: str) -> bool:
    text = raw.strip()
    if not text or "://" in text or text.startswith("#"):
        return True
    if text in ALLOW_PATHS or any(text.startswith(a) for a in ALLOW_PATHS if a.endswith("/")):
        return True
    if PLACEHOLDER_RE.search(text):
        # Treat templates with placeholders as OK when the template root exists.
        candidate = re.sub(r"<[^>]+>", "_TEMPLATE", text)
        candidate = candidate.replace("\\", "/")
        # Common journal/work-item template roots
        if "journals/work-items/" in candidate or "work-items/" in candidate:
            return (ROOT / "journals" / "work-items" / "_TEMPLATE").is_dir() or (
                ROOT / "work-items" / "_TEMPLATE"
            ).is_dir()
        return True
    # Only check repo-relative paths that look like files/dirs in this expert.
    if not re.match(r"^(\.cursor|facts|journals|work-items|docs|scripts|qa-sessions|MyRole|AGENTS|README|QUICK|DESIGN)", text):
        return True
    rel = text.replace("\\", "/").split()[0].rstrip(".,);:")
    return (ROOT / rel).exists()


def check_backtick_paths() -> None:
    files = [
        ROOT / "AGENTS.md",
        ROOT / "MyRole.txt",
        ROOT / "README.md",
        ROOT / "QUICK-START.md",
    ]
    files.extend((ROOT / ".cursor" / "skills").glob("*/SKILL.md"))
    files.extend((ROOT / ".cursor" / "workflows").glob("*.md"))
    for path in files:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for match in BACKTICK_PATH_RE.finditer(text):
            raw = match.group(1)
            if "/" not in raw and "\\" not in raw and not raw.endswith((".md", ".py", ".json", ".txt", ".mdc")):
                continue
            if not path_exists(raw):
                note(f"missing path in {path.relative_to(ROOT).as_posix()}: `{raw}`")


def check_registry() -> None:
    reg_path = ROOT / ".cursor" / "workflows" / "workflow-registry.json"
    data = json.loads(reg_path.read_text(encoding="utf-8"))
    workflows = data.get("workflows") if isinstance(data, dict) else None
    if not isinstance(workflows, dict):
        note("workflow-registry.json missing workflows object")
        return
    for key, entry in workflows.items():
        if not isinstance(entry, dict):
            continue
        rel = entry.get("instruction_file")
        if not isinstance(rel, str):
            note(f"workflow {key} missing instruction_file")
            continue
        if not (ROOT / rel).is_file():
            note(f"workflow {key} instruction_file missing: {rel}")


def check_triggers() -> None:
    known = load_known_tokens()
    if not known:
        return
    vocab_files = [
        ROOT / "facts" / "MEMORY-INDEX.md",
        ROOT / ".cursor" / "skills" / "remember" / "SKILL.md",
        ROOT / ".cursor" / "skills" / "promote-facts-rules" / "SKILL.md",
    ]
    token_re = re.compile(r"\b(write:[a-z0-9_-]+|sql:[a-z0-9_-]+|git:[a-z0-9_-]+|pr:[a-z0-9_-]+|config:[a-z0-9_-]+)\b")
    for path in vocab_files:
        if not path.is_file():
            continue
        for match in token_re.finditer(path.read_text(encoding="utf-8")):
            tok = match.group(1)
            if tok not in known and tok != "none":
                note(f"trigger `{tok}` in {path.relative_to(ROOT).as_posix()} not in KNOWN_TOKENS")


def check_escaped_and_stale() -> None:
    for path in ROOT.rglob("*.md"):
        if "node_modules" in path.parts:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            continue
        if ESCAPED_HEADING_RE.search(text):
            note(f"escaped heading in {path.relative_to(ROOT).as_posix()}")
        # Skip TRIGGER-INDEX generated content for inject-rules check after regen —
        # still flag if stale .sh remains.
        for pattern, label in STALE_PATTERNS:
            if pattern.search(text):
                # work-items facts/facts.md is a real relative path inside templates
                if "facts/facts.md" in label and "work-items" in path.as_posix():
                    continue
                note(f"{label} in {path.relative_to(ROOT).as_posix()}")


def check_readme_pair() -> None:
    readme = ROOT / "README.md"
    quick = ROOT / "QUICK-START.md"
    if readme.is_file() and quick.is_file():
        if readme.read_bytes() == quick.read_bytes():
            return
        # Role experts often keep a short README that points at QUICK-START.
        # Warn only when README does not mention QUICK-START.
        if "QUICK-START.md" not in readme.read_text(encoding="utf-8"):
            note("README.md and QUICK-START.md differ and README does not point at QUICK-START.md")


def main() -> int:
    check_canonical_skills()
    check_named_skills()
    check_backtick_paths()
    check_registry()
    check_triggers()
    check_escaped_and_stale()
    check_readme_pair()
    if FINDINGS:
        print(f"check_scaffold: {len(FINDINGS)} finding(s)")
        for item in FINDINGS:
            print(f" - {item}")
        return 1
    print("check_scaffold: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
