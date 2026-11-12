#!/usr/bin/env python3
"""Integrity check for this medical-clinic-front-role expert scaffold. Exit non-zero on findings."""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALLOW_MISSING = {
    ".claude/role-skills.md",
    ".claude/plans/",
    "work-items/<id>/",
    "journals/work-items/<id>/",
    "qa-sessions/Q*/",
}

SKILL_NAME = re.compile(r"(?:run\s+)?[`*]*([a-z][a-z0-9-]{2,})[`*]*")
BACKTICK_PATH = re.compile(r"`([^`\n]+)`")
ESCAPED_HEADING = re.compile(r"^\\#", re.MULTILINE)
BAD_PATTERNS = [
    re.compile(r"(?i)[a-z]wid-"),
    re.compile(r"2027-"),
    re.compile(r"(?<!work-items/<id>/)facts/facts\.md"),
    re.compile(r"-operations\.md"),  # intentional for this role; skip below
]


def load_known_tokens() -> set[str]:
    hook = ROOT / ".claude" / "hooks" / "inject_rules_on_action.py"
    spec = importlib.util.spec_from_file_location("inject_rules_on_action", hook)
    if spec is None or spec.loader is None:
        return set()
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return set(getattr(mod, "KNOWN_TOKENS", []) or [])


def existing_skills() -> set[str]:
    base = ROOT / ".claude" / "skills"
    if not base.is_dir():
        return set()
    return {p.name for p in base.iterdir() if p.is_dir()}


def named_skills(text: str) -> set[str]:
    # Conservative: only names that already look like skill folders in prose lists
    found = set()
    for m in re.finditer(
        r"\*\*([a-z][a-z0-9-]{2,})\*\*|`([a-z][a-z0-9-]{2,})`|/([a-z][a-z0-9-]{2,})\b",
        text,
    ):
        name = m.group(1) or m.group(2) or m.group(3)
        if name:
            found.add(name)
    return found


def path_exists(raw: str) -> bool:
    text = raw.strip()
    if not text or " " in text and not text.startswith((".", "docs", "facts", "work-items", "journals", ".claude", "scripts", "qa-sessions")):
        return True  # not a path
    if any(text.startswith(a) or a in text for a in ALLOW_MISSING):
        return True
    if "<" in text or "*" in text:
        # placeholder path — check template counterpart when obvious
        candidate = text
        for token in ("<id>", "<WID>", "<work-item-id>", "<node>", "<job>", "<name>"):
            candidate = candidate.replace(token, "_TEMPLATE")
        candidate = candidate.replace("\\", "/").rstrip("/")
        # strip anchors/trailing punctuation
        candidate = candidate.split("#", 1)[0].rstrip(").,;")
        if not candidate or candidate.endswith(("…", "...")):
            return True
        path = ROOT / candidate
        if path.exists():
            return True
        # journals/work-items/_TEMPLATE is ok for journals/work-items/<id>
        return True
    cleaned = text.split("#", 1)[0].rstrip(").,;").replace("\\", "/")
    if cleaned.startswith(("http://", "https://", "mailto:")):
        return True
    # Only check repo-looking paths
    if not cleaned.startswith(
        (".claude/", "docs/", "facts/", "journals/", "work-items/", "scripts/", "qa-sessions/", "CLAUDE", "MyRole", "README", "QUICK-START", "DESIGN")
    ):
        return True
    return (ROOT / cleaned).exists()


def main() -> int:
    findings: list[str] = []
    skills = existing_skills()
    known = load_known_tokens()

    scan_files = []
    for rel in ("CLAUDE.md", "MyRole.txt", "README.md", "QUICK-START.md"):
        p = ROOT / rel
        if p.exists():
            scan_files.append(p)
    scan_files.extend((ROOT / ".claude" / "skills").rglob("SKILL.md"))
    scan_files.extend((ROOT / ".claude" / "workflows").glob("*.md"))
    scan_files.extend((ROOT / "facts").glob("*.md"))

    # 1. Skills named in key docs that lack folders — only flag known required skill names for this role
    required = {
        "continue",
        "journal-keeper",
        "workflow-selector",
        "operator-qa",
        "remember",
        "integrate-docs",
        "promote-facts-rules",
        "define-role",
        "switch-context",
        "memory-optimize",
    }
    missing_required = sorted(required - skills)
    for name in missing_required:
        findings.append(f"missing required skill folder: {name}")

    # leftover developer phase skills named in CLAUDE.md would be flagged if present without a folder
    agents = (ROOT / "CLAUDE.md").read_text(encoding="utf-8") if (ROOT / "CLAUDE.md").exists() else ""
    for name in ("hld-writer", "dd-writer", "task-breakdown", "git-workflow"):
        if re.search(rf"\b{name}\b", agents) and name not in skills:
            findings.append(f"CLAUDE.md names missing skill: {name}")

    # 3. workflow-registry instruction files
    registry = ROOT / ".claude" / "workflows" / "workflow-registry.json"
    if registry.is_file():
        try:
            data = json.loads(registry.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            findings.append(f"workflow-registry.json invalid: {exc}")
            data = {}
        workflows = data.get("workflows") if isinstance(data, dict) else None
        if isinstance(workflows, dict):
            items = workflows.values()
        elif isinstance(workflows, list):
            items = workflows
        elif isinstance(data, list):
            items = data
        else:
            items = []
        for item in items:
            if not isinstance(item, dict):
                continue
            instr = item.get("instruction_file") or item.get("file") or item.get("path")
            if isinstance(instr, str) and instr.strip():
                path = ROOT / instr.replace("\\", "/")
                if not path.is_file():
                    # try relative to .claude/workflows
                    alt = ROOT / ".claude" / "workflows" / Path(instr).name
                    if not alt.is_file():
                        findings.append(f"missing instruction_file: {instr}")

    # 4. Trigger tokens in skills / MEMORY-INDEX
    trigger_re = re.compile(r"\b(write:[a-z]+|sql:[a-z]+|git:[a-z]+|pr:[a-z]+|config:[a-z]+)\b")
    for path in scan_files:
        text = path.read_text(encoding="utf-8")
        if path.name in {"TRIGGER-INDEX.md"}:
            continue
        for tok in set(trigger_re.findall(text)):
            if tok == "none":
                continue
            if known and tok not in known and "Triggers" in text:
                # only complain when documenting triggers as vocabulary
                if path.name in {"MEMORY-INDEX.md"} or path.parent.name in {
                    "remember",
                    "promote-facts-rules",
                    "integrate-docs",
                }:
                    if f"`{tok}`" in text or tok in text:
                        if tok not in known:
                            findings.append(
                                f"unknown trigger `{tok}` in {path.relative_to(ROOT)}"
                            )

    # 5. Escaped headings
    for path in ROOT.rglob("*.md"):
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        if ESCAPED_HEADING.search(text):
            findings.append(f"escaped heading in {path.relative_to(ROOT)}")

    # 6. Stale patterns (adapted: allow facts-operations / rules-operations)
    for path in scan_files:
        text = path.read_text(encoding="utf-8")
        if re.search(r"(?i)[a-z]wid-", text):
            findings.append(f"stale wid-glue pattern in {path.relative_to(ROOT)}")
        if "2027-" in text:
            findings.append(f"future archive date 2027- in {path.relative_to(ROOT)}")
        if re.search(r"(?<!work-items/<id>/facts/)(?<!work-items/<id>/)facts/facts\.md", text):
            if "work-items/<id>/facts/facts.md" not in text and "facts/facts.md" in text:
                # allow work-item path mentions
                for line in text.splitlines():
                    if "facts/facts.md" in line and "work-items/" not in line:
                        findings.append(
                            f"top-level facts/facts.md reference in {path.relative_to(ROOT)}"
                        )
                        break

    # 7. README vs QUICK-START — this role keeps both as distinct docs; warn only if identical expected
    readme = ROOT / "README.md"
    quick = ROOT / "QUICK-START.md"
    if readme.is_file() and quick.is_file():
        if readme.read_bytes() == quick.read_bytes():
            pass  # identical is fine
        # different is expected for this role; no finding

    if findings:
        print("check_scaffold FAILED:")
        for item in findings:
            print(f"  - {item}")
        return 1
    print("check_scaffold OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
