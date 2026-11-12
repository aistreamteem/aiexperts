#!/usr/bin/env python3
"""Integrity checks for this optometry-front-role Claude expert scaffold."""

from __future__ import annotations

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
}

SKILL_NAME_RE = re.compile(r"(?:run\s+)?([a-z][a-z0-9-]{2,})\b")
BACKTICK_PATH_RE = re.compile(r"`([^`]+)`")
ESCAPED_HEADING_RE = re.compile(r"^\\#", re.MULTILINE)
BAD_PATTERNS = [
    (re.compile(r"[a-z]wid-", re.I), "stale wid- splice"),
    (re.compile(r"2027-"), "future 2027- date"),
    (re.compile(r"facts/facts\.md"), "legacy facts/facts.md"),
    (re.compile(r"facts-operations\.md"), None),  # allowed
    (re.compile(r"-operations\.md"), None),
]


def _skills_on_disk() -> set[str]:
    base = ROOT / ".claude" / "skills"
    if not base.is_dir():
        return set()
    return {p.name for p in base.iterdir() if p.is_dir()}


def _named_skills() -> set[str]:
    names: set[str] = set()
    files = [
        ROOT / "CLAUDE.md",
        ROOT / "MyRole.txt",
        ROOT / "README.md",
        ROOT / "QUICK-START.md",
    ]
    files.extend((ROOT / ".claude" / "workflows").glob("*.md"))
    files.extend(ROOT.glob(".claude/skills/*/SKILL.md"))
    known = _skills_on_disk()
    for path in files:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for match in re.finditer(
            r"\*\*([a-z][a-z0-9-]{2,})\*\*|`([a-z][a-z0-9-]{2,})`|"
            r"(?:run\s+)([a-z][a-z0-9-]{2,})",
            text,
        ):
            name = next(g for g in match.groups() if g)
            if name in known or (ROOT / ".claude" / "skills" / name).is_dir():
                names.add(name)
            # Named required phase skills from AGENTS only when present as skills
            if name in {
                "hld-writer",
                "dd-writer",
                "task-breakdown",
                "git-workflow",
                "continue",
                "journal-keeper",
                "workflow-selector",
                "remember",
                "define-role",
                "promote-facts-rules",
                "operator-qa",
                "switch-context",
                "integrate-docs",
                "memory-optimize",
                "spec-parser",
            }:
                names.add(name)
    return names


def _known_tokens() -> list[str]:
    hook = ROOT / ".claude" / "hooks" / "inject_rules_on_action.py"
    text = hook.read_text(encoding="utf-8")
    match = re.search(r"KNOWN_TOKENS\s*=\s*\[(.*?)\]", text, re.S)
    if not match:
        return []
    return re.findall(r'"([^"]+)"', match.group(1))


def main() -> int:
    errors: list[str] = []
    on_disk = _skills_on_disk()
    for name in sorted(_named_skills()):
        if name not in on_disk and name in {
            "continue",
            "journal-keeper",
            "workflow-selector",
            "remember",
            "define-role",
            "promote-facts-rules",
            "operator-qa",
            "switch-context",
            "integrate-docs",
            "memory-optimize",
        }:
            errors.append(f"missing skill folder: {name}")

    registry = ROOT / ".claude" / "workflows" / "workflow-registry.json"
    if registry.is_file():
        data = json.loads(registry.read_text(encoding="utf-8"))
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
                if not path.is_file():
                    alt = ROOT / ".claude" / "workflows" / Path(instr).name
                    if not alt.is_file():
                        errors.append(f"missing workflow instruction: {instr}")

    known = set(_known_tokens()) | {"none"}
    for path in [ROOT / "facts" / "MEMORY-INDEX.md"]:
        path = path if path.is_file() else None
        if not path:
            continue
        text = path.read_text(encoding="utf-8")
        for tok in re.findall(r"`(write:[a-z]+|sql:[a-z]+|git:[a-z]+|pr:[a-z]+|config:[a-z]+)`", text):
            if tok not in known:
                errors.append(f"unknown trigger in MEMORY-INDEX.md: {tok}")

    for md in ROOT.rglob("*.md"):
        if "node_modules" in md.parts:
            continue
        text = md.read_text(encoding="utf-8", errors="replace")
        if ESCAPED_HEADING_RE.search(text):
            errors.append(f"escaped heading in {md.relative_to(ROOT)}")
        if re.search(r"[a-z]wid-", text, re.I) and "WID-" not in text[max(0, text.lower().find("wid-") - 1) :]:
            # flag workflowID- style splices only
            if re.search(r"workflowID-|folloWID-|newID-workflow", text):
                errors.append(f"stale ID splice in {md.relative_to(ROOT)}")
        if "2027-" in text:
            errors.append(f"future 2027- date in {md.relative_to(ROOT)}")
        for line in text.splitlines():
            if "facts/facts.md" not in line:
                continue
            if "work-items/" in line or "facts/facts-operations.md" in line:
                continue
            # Relative Work Item template links like (facts/facts.md) are fine.
            if "(facts/facts.md)" in line or "`facts/facts.md`" in line and "work-items" in str(md):
                continue
            if md.parts[:2] == ("work-items", "_TEMPLATE"):
                continue
            errors.append(
                f"legacy facts/facts.md in {md.relative_to(ROOT)}: {line.strip()[:80]}"
            )
            break

    readme = ROOT / "README.md"
    quick = ROOT / "QUICK-START.md"
    if readme.is_file() and quick.is_file():
        readme_text = readme.read_text(encoding="utf-8")
        quick_text = quick.read_text(encoding="utf-8")
        if readme_text != quick_text:
            points = "QUICK-START.md" in readme_text and len(readme_text) < 2000
            if not points and len(readme_text) > 500 and len(quick_text) > 500:
                errors.append("README.md and QUICK-START.md differ")

    if errors:
        print("scaffold check FAILED:")
        for err in errors:
            print(f"  - {err}")
        return 1
    print("scaffold check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
