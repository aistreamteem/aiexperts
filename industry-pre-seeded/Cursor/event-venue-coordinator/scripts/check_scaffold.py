#!/usr/bin/env python3
"""Integrity check for this role expert scaffold. Exit non-zero on findings."""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALLOW_MISSING = {
    ".cursor/role-skills.md",
    ".cursor/active-work-item.txt",
    "work-items/<id>/journal/progress.md",
}
SKILL_NAME_RE = re.compile(
    r"\b(define-role|continue|workflow-selector|journal-keeper|remember|"
    r"promote-facts-rules|integrate-docs|memory-optimize|operator-qa|"
    r"switch-context|visual-page|spec-parser|implement-feature|"
    r"iterative-feature|refactor|scaffold-project|diagram-generator|"
    r"hld-writer|dd-writer|task-breakdown|git-workflow)\b"
)
BACKTICK_PATH_RE = re.compile(r"`([^`]+)`")
ESCAPED_HEADING_RE = re.compile(r"^\\#", re.M)
BAD_PATTERNS = [
    (re.compile(r"(?i)[a-z]wid-"), "mangled ...WID- fragment"),
    (re.compile(r"2027-"), "future archive date 2027-"),
    (re.compile(r"facts/facts\.md"), "top-level facts/facts.md"),
    (re.compile(r"-operations\.md"), "legacy operations memory filename"),
]


def fail(findings: list[str], message: str) -> None:
    findings.append(message)


def load_known_tokens() -> set[str]:
    hook = ROOT / ".cursor" / "hooks" / "inject_rules_on_action.py"
    spec = importlib.util.spec_from_file_location("inject_rules_on_action", hook)
    if spec is None or spec.loader is None:
        return set()
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return set(getattr(module, "KNOWN_TOKENS", []) or [])


def skill_exists(name: str) -> bool:
    return (ROOT / ".cursor" / "skills" / name / "SKILL.md").is_file()


def path_exists(raw: str) -> bool:
    text = raw.strip()
    if text in ALLOW_MISSING:
        return True
    if any(ch in text for ch in ["<", "*", "|", "http://", "https://"]):
        # Placeholder or URL-like; treat templates as ok when parent template exists.
        candidate = text
        for token in ("<id>", "<WID>", "<work-item-id>", "<context_id>", "<node>", "<node-id>", "<label>", "<topic>", "<name>"):
            candidate = candidate.replace(token, "_TEMPLATE")
        candidate = candidate.replace("WID-XXXXXXXX", "_TEMPLATE")
        path = ROOT / candidate
        if path.exists():
            return True
        # journals/work-items/<id>/... → journals/work-items/_TEMPLATE/...
        alt = text
        for token in ("<id>", "<WID>", "<work-item-id>", "<context_id>"):
            alt = alt.replace(token, "_TEMPLATE")
        return (ROOT / alt).exists() or "/" not in text
    return (ROOT / text).exists()


def main() -> int:
    findings: list[str] = []
    md_files = list(ROOT.rglob("*.md")) + [ROOT / "AGENTS.md", ROOT / "MyRole.txt"]
    md_files = [p for p in md_files if p.is_file() and "__pycache__" not in p.parts]

    # 1. Skill names referenced have folders
    named: set[str] = set()
    for path in md_files:
        text = path.read_text(encoding="utf-8", errors="replace")
        named.update(SKILL_NAME_RE.findall(text))
    # Role does not use developer design-phase skills; ignore those names if absent.
    skip_if_missing = {"hld-writer", "dd-writer", "task-breakdown", "git-workflow"}
    for name in sorted(named):
        if skill_exists(name):
            continue
        if name in skip_if_missing:
            continue
        fail(findings, f"missing skill folder for referenced skill `{name}`")

    # 2. Backticked repo paths (best-effort)
    for path in md_files:
        rel = path.relative_to(ROOT).as_posix()
        if rel.startswith("facts/TRIGGER-INDEX.md"):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for match in BACKTICK_PATH_RE.finditer(text):
            raw = match.group(1)
            if "/" not in raw and "\\" not in raw:
                continue
            if raw.startswith(("http://", "https://", "docs/tools/", "gh ")):
                continue
            # Skip developer/incident leftovers this venue role does not ship.
            norm = raw.replace("\\", "/")
            if norm.startswith(("docs/design/", "docs/incident/")):
                continue
            if any(norm.startswith(prefix) for prefix in (".cursor/skills/", "facts/", "journals/", "work-items/", "scripts/", "docs/", "qa-sessions/")):
                if not path_exists(norm):
                    if "<" not in norm and "*" not in norm:
                        candidate = ROOT / norm
                        if not candidate.exists() and norm.endswith((".md", ".py", ".json", ".txt", ".mdc")):
                            fail(findings, f"{rel}: missing path `{raw}`")

    # 3. workflow-registry instruction files
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
                    if not (ROOT / instr).is_file():
                        fail(findings, f"registry instruction missing: {instr}")
        # memory pointers
        for key in ("facts", "rules"):
            pointer = data.get(key)
            if isinstance(pointer, str) and pointer and not (ROOT / pointer).is_file():
                fail(findings, f"registry {key} missing: {pointer}")

    # 4. Trigger tokens in skills / MEMORY-INDEX are known
    known = load_known_tokens()
    trigger_re = re.compile(r"\b(write:doc|write:csv|write:sql|sql:generate|pr:open|git:push|git:commit|config:change)\b")
    for path in md_files:
        if path.name == "TRIGGER-INDEX.md":
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for tok in set(trigger_re.findall(text)):
            if known and tok not in known and tok != "none":
                fail(findings, f"{path.relative_to(ROOT)}: unknown trigger `{tok}`")

    # 5. No escaped headings
    for path in md_files:
        text = path.read_text(encoding="utf-8", errors="replace")
        if ESCAPED_HEADING_RE.search(text):
            fail(findings, f"{path.relative_to(ROOT)}: escaped heading \\#")

    # 6. Stale patterns
    for path in md_files:
        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8", errors="replace")
        for cre, label in BAD_PATTERNS:
            if cre.search(text):
                # Allow work-item facts/facts.md references
                if label.startswith("top-level") and "work-items/" in text and "facts/facts.md" in text:
                    # only fail if a non-work-item absolute style remains; soft-check line by line
                    for i, line in enumerate(text.splitlines(), 1):
                        if "facts/facts.md" in line and "work-items/" not in line and "`facts/facts.md`" in line:
                            fail(findings, f"{rel}:{i}: {label}")
                    continue
                fail(findings, f"{rel}: {label}")

    # 7. README / QUICK-START identical if both exist
    readme = ROOT / "README.md"
    quick = ROOT / "QUICK-START.md"
    if readme.is_file() and quick.is_file():
        if readme.read_text(encoding="utf-8") != quick.read_text(encoding="utf-8"):
            fail(findings, "README.md and QUICK-START.md differ")

    if findings:
        print("check_scaffold FAILED:")
        for item in findings:
            print(f"- {item}")
        return 1
    print("check_scaffold OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
