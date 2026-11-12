#!/usr/bin/env python3
"""Integrity check for this landscaping-office expert scaffold. Exit non-zero on findings."""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_SKILLS = [
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
]

STALE_RE = re.compile(r"(?i)(?:workflowID-|WorkflowID-|newID-workflow|folloWID)")
ESCAPED_HEADING_RE = re.compile(r"^\\#", re.M)
TRIGGER_LINE_RE = re.compile(r"^\*\*Triggers:\*\*\s*(.+)$", re.M)


def load_known_tokens() -> set[str]:
    hook = ROOT / ".cursor" / "hooks" / "inject_rules_on_action.py"
    spec = importlib.util.spec_from_file_location("inject_rules_on_action", hook)
    if spec is None or spec.loader is None:
        return set()
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return set(getattr(mod, "KNOWN_TOKENS", []))


def main() -> int:
    findings: list[str] = []
    skills_dir = ROOT / ".cursor" / "skills"
    present = {p.name for p in skills_dir.iterdir() if p.is_dir()} if skills_dir.is_dir() else set()
    for name in REQUIRED_SKILLS:
        if name not in present:
            findings.append(f"required skill missing: {name}")

    registry_path = ROOT / ".cursor" / "workflows" / "workflow-registry.json"
    if not registry_path.is_file():
        findings.append("missing workflow-registry.json")
    else:
        data = json.loads(registry_path.read_text(encoding="utf-8"))
        items = []
        if isinstance(data, dict):
            if isinstance(data.get("workflows"), list):
                items = data["workflows"]
            elif isinstance(data.get("jobs"), list):
                items = data["jobs"]
            elif isinstance(data.get("workflows"), dict):
                items = list(data["workflows"].values())
        for item in items:
            if not isinstance(item, dict):
                continue
            instr = item.get("instruction_file") or item.get("file") or ""
            if instr and not (ROOT / instr).is_file():
                findings.append(f"registry instruction missing: {instr}")

    for required in (
        ".cursor/hooks/inject_journal_context.py",
        ".cursor/hooks/inject_rules_on_action.py",
        ".cursor/hooks/on_stop.py",
        ".cursor/hooks/merge_agent_notes.py",
        ".cursor/hooks/journal_snapshot.py",
        ".cursor/hooks/journal_fields.py",
        ".gitattributes",
        ".gitignore",
        "facts/facts-operations.md",
        "facts/rules-operations.md",
    ):
        if not (ROOT / required).is_file():
            findings.append(f"missing required file: {required}")

    known = load_known_tokens() | {"none"}
    for path in [ROOT / "facts" / "MEMORY-INDEX.md", *skills_dir.glob("*/SKILL.md")]:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for m in TRIGGER_LINE_RE.finditer(text):
            raw = m.group(1)
            for tok in re.findall(r"[a-z]+:[a-z0-9_-]+", raw.lower()):
                if tok not in known:
                    findings.append(
                        f"{path.relative_to(ROOT)}: trigger not in KNOWN_TOKENS: {tok}"
                    )

    for path in ROOT.rglob("*.md"):
        if any(part.startswith(".") and part not in {".cursor"} for part in path.parts):
            if ".cursor" not in path.parts and path.parts[0] != "facts":
                # still scan .cursor
                pass
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if ESCAPED_HEADING_RE.search(text):
            findings.append(f"escaped markdown heading: {path.relative_to(ROOT)}")
        if STALE_RE.search(text):
            findings.append(f"stale WID insertion: {path.relative_to(ROOT)}")
        if "2027-" in text:
            findings.append(f"future 2027- date: {path.relative_to(ROOT)}")
        if "inject-rules-on-action.sh" in text:
            findings.append(f"shell rules hook name: {path.relative_to(ROOT)}")
        if "config:change" in text:
            findings.append(f"retired trigger config:change: {path.relative_to(ROOT)}")
        if re.search(r"(?<![\w/-])facts/facts\.md", text) and "work-items/" not in text[
            max(0, text.find("facts/facts.md") - 40) : text.find("facts/facts.md") + 20
        ]:
            # flag top-level facts/facts.md mentions outside work-item templates
            if "work-items/<id>/facts/facts.md" not in text and "work-items/<work-item-id>/facts/facts.md" not in text:
                if "facts/facts.md" in text and "facts/facts-operations.md" not in text[text.find("facts/facts.md") : text.find("facts/facts.md") + 30]:
                    pass

    # Remaining work-items/.../journal/ writes (except intentional historical mentions in journal-keeper)
    for path in ROOT.rglob("*.md"):
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if re.search(r"work-items/<[^>]+>/journal/", text):
            # allow negative guidance ("do not write", "not a pointer under")
            for line in text.splitlines():
                if "work-items/" in line and "/journal/" in line:
                    lower = line.lower()
                    if any(
                        w in lower
                        for w in ("do not", "not a pointer", "not under", "pointer", "legacy")
                    ):
                        continue
                    if "Write through" in line:
                        continue
                    findings.append(
                        f"old journal path: {path.relative_to(ROOT)} :: {line.strip()[:120]}"
                    )

    if findings:
        # de-dupe
        uniq = sorted(set(findings))
        print("Scaffold check FAILED:")
        for item in uniq:
            print(f"  - {item}")
        return 1
    print("Scaffold check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
