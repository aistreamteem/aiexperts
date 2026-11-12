#!/usr/bin/env python3
"""Integrity check for this Cursor role expert scaffold.

Exits non-zero on any finding. Stdlib only.
"""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SKILL_NAME_RE = re.compile(
    r"\b(define-role|continue|workflow-selector|journal-keeper|remember|"
    r"promote-facts-rules|integrate-docs|memory-optimize|operator-qa|"
    r"switch-context|visual-page|spec-parser|implement-feature|"
    r"iterative-feature|refactor|scaffold-project|diagram-generator|"
    r"hld-writer|dd-writer|task-breakdown|git-workflow)\b"
)

BACKTICK_PATH_RE = re.compile(r"`([^`]+)`")
PLACEHOLDER_RE = re.compile(r"<[^>]+>|WID-\*|WID-X+")
ESCAPED_HEADING_RE = re.compile(r"(?m)^\\#")
# Runtime / template paths that may not exist yet
ALLOW_PATHS = {
    ".cursor/role-skills.md",
    ".cursor/active-context.txt",
    ".cursor/active-work-item.txt",
    ".cursor/plans/",
    "work-items/<id>/",
    "journals/work-items/<id>/",
    "qa-sessions/Q*/",
}

REQUIRED_SKILLS_FROM_AGENTS = [
    "define-role",
    "continue",
    "workflow-selector",
    "journal-keeper",
    "remember",
    "promote-facts-rules",
    "operator-qa",
    "switch-context",
]


def _load_known_tokens() -> list[str]:
    hook = ROOT / ".cursor" / "hooks" / "inject_rules_on_action.py"
    spec = importlib.util.spec_from_file_location("inject_rules_on_action", hook)
    if spec is None or spec.loader is None:
        return []
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    tokens = getattr(mod, "KNOWN_TOKENS", [])
    return list(tokens) if isinstance(tokens, list) else []


def _exists_with_placeholder(path_text: str) -> bool:
    cleaned = path_text.strip().strip("`")
    if cleaned in ALLOW_PATHS or any(cleaned.startswith(a) for a in ALLOW_PATHS):
        return True
    if cleaned.startswith("http://") or cleaned.startswith("https://"):
        return True
    # Ignore pure tokens / commands
    if "/" not in cleaned and "\\" not in cleaned:
        return True
    if " " in cleaned and not cleaned.startswith(".") and not cleaned.startswith("facts/"):
        return True
    rel = PLACEHOLDER_RE.sub("*", cleaned).replace("\\", "/")
    # Template wildcards → check parent template dirs
    if "*" in rel:
        # e.g. work-items/*/facts/facts.md → work-items/_TEMPLATE/facts/facts.md
        parts = rel.split("/")
        trial = []
        for part in parts:
            if part == "*":
                trial.append("_TEMPLATE")
            else:
                trial.append(part)
        candidate = ROOT.joinpath(*trial)
        if candidate.exists():
            return True
        # Also accept journals/work-items/_TEMPLATE/...
        return True  # placeholders are soft
    return (ROOT / rel).exists()


def main() -> int:
    findings: list[str] = []

    # 1. Skills named in AGENTS.md exist
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    for name in REQUIRED_SKILLS_FROM_AGENTS:
        if name in agents or f"**{name}**" in agents or name.replace("-", " ") in agents.lower():
            folder = ROOT / ".cursor" / "skills" / name / "SKILL.md"
            if not folder.is_file():
                findings.append(f"missing skill folder for AGENTS reference: {name}")
    # Also every skill folder under .cursor/skills must have SKILL.md
    skills_root = ROOT / ".cursor" / "skills"
    if skills_root.is_dir():
        for child in skills_root.iterdir():
            if child.is_dir() and not (child / "SKILL.md").is_file():
                findings.append(f"skill folder missing SKILL.md: {child.name}")

    # Named developer phase skills must NOT be required for this role
    for banned in ("hld-writer", "dd-writer", "task-breakdown", "git-workflow"):
        if (skills_root / banned).is_dir():
            findings.append(f"unexpected developer phase skill present: {banned}")

    # 2. Soft path check on AGENTS.md / MyRole.txt / key skills
    for rel in (
        "AGENTS.md",
        "MyRole.txt",
        ".cursor/CONTEXT-SYSTEM.md",
        "facts/MEMORY-INDEX.md",
    ):
        text = (ROOT / rel).read_text(encoding="utf-8")
        for match in BACKTICK_PATH_RE.findall(text):
            if not any(ch in match for ch in "/\\"):
                continue
            if match.endswith(".md") or match.endswith(".json") or match.endswith(".txt") or match.endswith(".py"):
                if not _exists_with_placeholder(match):
                    findings.append(f"missing path in {rel}: `{match}`")

    # 3. workflow-registry instruction files exist
    registry = ROOT / ".cursor" / "workflows" / "workflow-registry.json"
    if registry.is_file():
        data = json.loads(registry.read_text(encoding="utf-8"))
        workflows = data.get("workflows") if isinstance(data, dict) else None
        if isinstance(workflows, list):
            for entry in workflows:
                if not isinstance(entry, dict):
                    continue
                instr = entry.get("instruction_file") or entry.get("file")
                if isinstance(instr, str) and instr.strip():
                    path = ROOT / instr.replace("\\", "/")
                    if not path.is_file():
                        # try under .cursor/workflows
                        alt = ROOT / ".cursor" / "workflows" / Path(instr).name
                        if not alt.is_file():
                            findings.append(f"registry instruction missing: {instr}")

    # 4. Trigger tokens in MEMORY-INDEX / remember / promote are known
    known = set(_load_known_tokens()) | {"none"}
    for rel in (
        "facts/MEMORY-INDEX.md",
        ".cursor/skills/remember/SKILL.md",
        ".cursor/skills/promote-facts-rules/SKILL.md",
    ):
        text = (ROOT / rel).read_text(encoding="utf-8")
        for tok in re.findall(r"\b(?:write|sql|git|pr|config):[a-z0-9_-]+\b", text):
            if tok not in known:
                findings.append(f"unknown trigger token `{tok}` in {rel}")

    # 5. No escaped markdown headings
    for path in ROOT.rglob("*.md"):
        if "node_modules" in path.parts:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if ESCAPED_HEADING_RE.search(text):
            findings.append(f"escaped heading in {path.relative_to(ROOT)}")

    # 6. Stale text patterns (narrowed for this role)
    stale = [
        (re.compile(r"workflowID-"), "corrupted workflowID- fragment"),
        (re.compile(r"WorkflowID-"), "corrupted WorkflowID- fragment"),
        (re.compile(r"newID-workflow"), "corrupted newID-workflow fragment"),
        (re.compile(r"2027-"), "future archive date 2027-"),
        (re.compile(r"inject-rules-on-action\.sh"), "legacy rules hook .sh name"),
        (re.compile(r"(?<![\w/-])facts/facts\.md"), "legacy top-level facts/facts.md"),
    ]
    skip_names = {"TRIGGER-INDEX.md", "trigger-index.json", "check_scaffold.py"}
    for path in ROOT.rglob("*"):
        if path.suffix.lower() not in {".md", ".py", ".txt", ".json"}:
            continue
        if path.name in skip_names:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for pattern, label in stale:
            if pattern.search(text):
                findings.append(f"{label} in {path.relative_to(ROOT)}")
                break

    # 7. README vs QUICK-START: this role keeps distinct short docs — warn only if one is empty
    readme = ROOT / "README.md"
    quick = ROOT / "QUICK-START.md"
    if readme.is_file() and quick.is_file():
        if not readme.read_text(encoding="utf-8").strip() or not quick.read_text(encoding="utf-8").strip():
            findings.append("README.md or QUICK-START.md is empty")

    if findings:
        print("check_scaffold FAILED:")
        for item in findings:
            print(f"  - {item}")
        return 1
    print("check_scaffold OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
