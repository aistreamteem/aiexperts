#!/usr/bin/env python3
"""Integrity check for this role expert scaffold. Exit non-zero on findings."""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FINDINGS: list[str] = []


def note(msg: str) -> None:
    FINDINGS.append(msg)


def _load_known_tokens() -> set[str]:
    hook = ROOT / ".claude" / "hooks" / "inject_rules_on_action.py"
    spec = importlib.util.spec_from_file_location("inject_rules_on_action", hook)
    if spec is None or spec.loader is None:
        return set()
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return set(getattr(mod, "KNOWN_TOKENS", []) or [])


def check_skills_exist() -> None:
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
        if not (ROOT / ".claude" / "skills" / name / "SKILL.md").is_file():
            note(f"missing skill folder: {name}")


def check_registry() -> None:
    reg = ROOT / ".claude" / "workflows" / "workflow-registry.json"
    data = json.loads(reg.read_text(encoding="utf-8"))
    items = data.get("workflows", data)
    if isinstance(items, dict):
        iterable = items.items()
        for key, meta in iterable:
            if key in {"default_workflow", "facts", "rules", "version"}:
                continue
            if not isinstance(meta, dict):
                continue
            instr = meta.get("instruction_file") or meta.get("file")
            if not instr:
                continue
            cand = [
                ROOT / ".claude" / "workflows" / Path(str(instr)).name,
                ROOT / str(instr),
            ]
            if not any(p.is_file() for p in cand):
                note(f"registry instruction missing for {key}: {instr}")
    elif isinstance(items, list):
        for meta in items:
            if not isinstance(meta, dict):
                continue
            instr = meta.get("instruction_file") or meta.get("file")
            wid = meta.get("id") or meta.get("name")
            if instr:
                cand = [
                    ROOT / ".claude" / "workflows" / Path(str(instr)).name,
                    ROOT / str(instr),
                ]
                if not any(p.is_file() for p in cand):
                    note(f"registry instruction missing for {wid}: {instr}")


def check_triggers() -> None:
    known = _load_known_tokens()
    if not known:
        note("KNOWN_TOKENS empty or unloadable")
        return
    pattern = re.compile(
        r"\b(write:[a-z0-9-]+|sql:[a-z0-9-]+|git:[a-z0-9-]+|pr:[a-z0-9-]+|config:[a-z0-9-]+)\b"
    )
    for path in [
        ROOT / ".claude" / "skills" / "remember" / "SKILL.md",
        ROOT / ".claude" / "skills" / "promote-facts-rules" / "SKILL.md",
        ROOT / "facts" / "MEMORY-INDEX.md",
    ]:
        text = path.read_text(encoding="utf-8")
        for tok in pattern.findall(text):
            if tok != "none" and tok not in known:
                note(f"trigger {tok} in {path.name} not in KNOWN_TOKENS")


def check_escaped_markdown() -> None:
    for path in ROOT.rglob("*.md"):
        if "visual-page" in str(path):
            continue
        for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if line.lstrip().startswith(r"\#"):
                note(f"escaped heading {path.relative_to(ROOT)}:{i}")


def check_stale_patterns() -> None:
    skip_names = {
        "TRIGGER-INDEX.md",
        "trigger-index.json",
        "test_rules_hook.py",
        "check_scaffold.py",
        "inject_rules_on_action.py",
    }
    for path in ROOT.rglob("*"):
        if path.suffix.lower() not in {".md", ".txt", ".py", ".json"}:
            continue
        if path.name in skip_names or "visual-page" in str(path):
            continue
        rel = str(path.relative_to(ROOT)).replace("\\", "/")
        if rel.startswith("work-items/") and (
            rel.endswith("facts/facts.md") or rel.endswith("STATUS.md")
        ):
            # Work Item templates legitimately name relative facts/facts.md
            pass_facts = True
        else:
            pass_facts = False
        text = path.read_text(encoding="utf-8")
        if re.search(r"(?<![A-Za-z])[a-z]wid-", text, re.I):
            note(f"stale wid- splice in {rel}")
            continue
        if "2027-" in text:
            note(f"future 2027- date in {rel}")
            continue
        if not pass_facts:
            bare_facts = False
            for m in re.finditer(r"facts/facts\.md", text):
                window = text[max(0, m.start() - 48) : m.start()]
                if "work-items/" not in window:
                    bare_facts = True
                    break
            if bare_facts:
                note(f"top-level facts/facts.md in {rel}")
                continue
        if re.search(r"(facts|rules)-operations\.md", text):
            note(f"operations memory filename in {rel}")
            continue
        if "config:change" in text and "no config:change" not in text.lower():
            note(f"retired config:change trigger in {rel}")
            continue
        if "workflowID-" in text:
            note(f"workflowID- splice in {rel}")
            continue
        if re.search(r"work-items/.+/journal/", text):
            note(f"legacy work-items journal path in {rel}")
            continue


def main() -> int:
    check_skills_exist()
    check_registry()
    check_triggers()
    check_escaped_markdown()
    check_stale_patterns()
    if FINDINGS:
        print("Scaffold check FAILED:")
        for f in FINDINGS:
            print(f" - {f}")
        return 1
    print("Scaffold check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
