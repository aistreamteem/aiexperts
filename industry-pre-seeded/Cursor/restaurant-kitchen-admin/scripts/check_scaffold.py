"""Integrity checks for the restaurant-kitchen-admin Cursor expert scaffold."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALLOW_MISSING = {
    ".cursor/role-skills.md",
    ".cursor/active-work-item.txt",
    "work-items/<id>/NEEDS-ATTENTION.md",
}
SKILL_NAME = re.compile(r"(?:run |skill |/)([a-z][a-z0-9-]+)")
BACKTICK_PATH = re.compile(r"`([^`]+)`")
PLACEHOLDER = re.compile(r"<(?:id|WID|work-item-id|node|[^>]+)>", re.I)
ESCAPED_HASH = re.compile(r"^\\#", re.M)
BAD_PATTERNS = [
    re.compile(r"(?i)[a-z]wid-"),
    re.compile(r"2027-"),
    re.compile(r"facts/facts\.md"),
    re.compile(r"-operations\.md"),  # only flag when paired wrongly; see below
]


def _skills_on_disk() -> set[str]:
    base = ROOT / ".cursor" / "skills"
    if not base.is_dir():
        return set()
    return {p.name for p in base.iterdir() if p.is_dir()}


def _named_skills() -> set[str]:
    names: set[str] = set()
    files = [
        ROOT / "AGENTS.md",
        ROOT / "MyRole.txt",
        ROOT / "README.md",
        * (ROOT / ".cursor" / "skills").glob("*/SKILL.md"),
        * (ROOT / ".cursor" / "workflows").glob("*.md"),
    ]
    for path in files:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for match in re.finditer(r"\*\*([a-z][a-z0-9-]+)\*\*", text):
            names.add(match.group(1))
        for match in re.finditer(r"`\.cursor/skills/([a-z][a-z0-9-]+)`", text):
            names.add(match.group(1))
    # Only keep names that look like skill folders we care about when mentioned as skills
    return names


def _path_exists(raw: str) -> bool:
    text = raw.strip()
    if not text or " " in text or text.startswith("http"):
        return True
    if text in ALLOW_MISSING:
        return True
    if any(ch in text for ch in "*?|"):
        return True
    if text.startswith("work-item:"):
        return True
    candidate = text.replace("\\", "/")
    if PLACEHOLDER.search(candidate):
        # Map to templates when possible
        if "journals/work-items/" in candidate:
            return (ROOT / "journals" / "work-items" / "_TEMPLATE").is_dir()
        if candidate.startswith("work-items/"):
            return (ROOT / "work-items" / "_TEMPLATE").is_dir()
        if candidate.startswith(".cursor/skills/"):
            return True
        return True
    path = ROOT / candidate
    return path.exists()


def main() -> int:
    findings: list[str] = []
    on_disk = _skills_on_disk()
    # Skills named by kitchen AGENTS / MyRole operating loop
    required = {
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
    for name in sorted(required):
        if name not in on_disk:
            findings.append(f"missing skill folder: {name}")

    registry = ROOT / ".cursor" / "workflows" / "workflow-registry.json"
    if registry.is_file():
        data = json.loads(registry.read_text(encoding="utf-8"))
        workflows = data.get("workflows") if isinstance(data, dict) else data
        entries: list[dict] = []
        if isinstance(workflows, list):
            entries = [e for e in workflows if isinstance(e, dict)]
        elif isinstance(workflows, dict):
            entries = [e for e in workflows.values() if isinstance(e, dict)]
        for entry in entries:
            instr = entry.get("instruction_file") or entry.get("file")
            if isinstance(instr, str) and instr.strip():
                path = ROOT / instr.replace("\\", "/")
                if not path.is_file():
                    alt = ROOT / ".cursor" / "workflows" / Path(instr).name
                    if not alt.is_file():
                        findings.append(f"missing workflow file: {instr}")

    # Trigger tokens in docs vs hook
    hook = ROOT / ".cursor" / "hooks" / "inject_rules_on_action.py"
    known: set[str] = set()
    if hook.is_file():
        ns: dict = {}
        exec(hook.read_text(encoding="utf-8"), ns)
        tokens = ns.get("KNOWN_TOKENS")
        if isinstance(tokens, list):
            known = set(tokens)
    for path in [
        ROOT / "facts" / "MEMORY-INDEX.md",
        * (ROOT / ".cursor" / "skills").glob("*/SKILL.md"),
    ]:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for match in re.finditer(
            r"`((?:write|sql|git|pr|config|file):[a-z-]+)`", text
        ):
            tok = match.group(1)
            if tok != "none" and known and tok not in known:
                findings.append(f"unknown trigger {tok} in {path.relative_to(ROOT)}")

    for path in ROOT.rglob("*.md"):
        if "node_modules" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        if ESCAPED_HASH.search(text):
            findings.append(f"escaped heading in {path.relative_to(ROOT)}")
        if re.search(r"(?i)[a-z]wid-", text):
            findings.append(f"workflowID leftover in {path.relative_to(ROOT)}")
        if "2027-" in text:
            findings.append(f"future date 2027 in {path.relative_to(ROOT)}")

    readme = ROOT / "README.md"
    quick = ROOT / "QUICK-START.md"
    if readme.is_file() and quick.is_file():
        if readme.read_text(encoding="utf-8") != quick.read_text(encoding="utf-8"):
            findings.append("README.md and QUICK-START.md differ")

    if findings:
        print("Scaffold check FAILED:")
        for item in findings:
            print(f"  - {item}")
        return 1
    print("Scaffold check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
