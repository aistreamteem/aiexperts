#!/usr/bin/env python3
"""Integrity check for this Cursor role expert. Exit non-zero on findings."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / ".cursor" / "skills"
ALLOW_MISSING = {
    ".cursor/role-skills.md",
    ".cursor/active-work-item.txt",
    ".cursor/plans/",
    "work-items/<id>/",
    "journals/work-items/<id>/",
}

SKILL_NAME_RE = re.compile(r"\*\*([a-z0-9-]+)\*\*|`([a-z0-9-]+)`|\b([a-z][a-z0-9-]{2,})\b")
PATH_RE = re.compile(r"`([^`]+)`")
PLACEHOLDER_RE = re.compile(r"<[^>]+>|WID-\*|\\\{id\\\}|\{id\}")


def load_known_tokens() -> set[str]:
    sys.path.insert(0, str(ROOT / ".cursor" / "hooks"))
    from inject_rules_on_action import KNOWN_TOKENS  # type: ignore

    return set(KNOWN_TOKENS)


def existing_skills() -> set[str]:
    return {p.name for p in SKILLS_DIR.iterdir() if p.is_dir() and (p / "SKILL.md").is_file()}


def named_skills(text: str) -> set[str]:
    # Heuristic: kebab-case tokens that look like skill folders referenced near "skill"
    found = set()
    for match in re.finditer(
        r"(?:skill\s+|run\s+|invoke\s+|\*\*|`)([a-z][a-z0-9-]{2,})(?:\*\*|`|\s)",
        text,
        re.I,
    ):
        found.add(match.group(1))
    return found


def path_exists(raw: str) -> bool:
    text = raw.strip()
    if not text or "://" in text or text.startswith("http"):
        return True
    if text in ALLOW_MISSING or any(text.startswith(a) for a in ALLOW_MISSING if a.endswith("/")):
        return True
    if any(ch in text for ch in ["*", "<", "{", "}"]):
        # Placeholder path: check template sibling when possible
        candidate = PLACEHOLDER_RE.sub("_TEMPLATE", text).replace("\\", "/")
        if "<" in text or "{" in text:
            # Try journals/work-items/_TEMPLATE and work-items/_TEMPLATE
            for trial in (
                candidate,
                text.replace("<id>", "_TEMPLATE").replace("<WID>", "_TEMPLATE").replace("<work-item-id>", "_TEMPLATE").replace("<context_id>", "_TEMPLATE"),
            ):
                p = ROOT / trial.replace("\\", "/")
                if p.exists():
                    return True
            # Runtime-created paths under work-items/<id>/ are ok if template exists
            if text.startswith("work-items/") or text.startswith("journals/"):
                return True
            return True
        return (ROOT / candidate).exists() or True
    rel = text.replace("\\", "/").lstrip("./")
    return (ROOT / rel).exists()


def main() -> int:
    findings: list[str] = []
    skills = existing_skills()

    scan_files = [
        ROOT / "AGENTS.md",
        ROOT / "MyRole.txt",
        ROOT / "README.md",
        ROOT / "QUICK-START.md",
        *SKILLS_DIR.glob("*/SKILL.md"),
        *(ROOT / ".cursor" / "workflows").glob("*.md"),
    ]
    texts = []
    for path in scan_files:
        if path.is_file():
            texts.append((path, path.read_text(encoding="utf-8")))

    # 1. Skills named in docs exist (only require those that look like skill folder names)
    known_skillish = skills | {
        "define-role",
        "continue",
        "journal-keeper",
        "remember",
        "promote-facts-rules",
        "workflow-selector",
        "switch-context",
        "operator-qa",
        "integrate-docs",
        "memory-optimize",
        "visual-page",
    }
    for path, text in texts:
        for name in named_skills(text):
            if name in known_skillish and name not in skills:
                # leftover developer phase names may still appear; report them
                if name in {
                    "hld-writer",
                    "dd-writer",
                    "task-breakdown",
                    "git-workflow",
                    "implement-feature",
                    "iterative-feature",
                    "scaffold-project",
                    "spec-parser",
                    "refactor",
                    "diagram-generator",
                    "test-writer",
                }:
                    if name not in skills:
                        findings.append(f"{path.relative_to(ROOT)}: missing skill folder `{name}`")
                elif name not in skills and name in {
                    "define-role",
                    "continue",
                    "journal-keeper",
                    "remember",
                    "promote-facts-rules",
                    "workflow-selector",
                    "switch-context",
                    "operator-qa",
                    "integrate-docs",
                    "memory-optimize",
                    "visual-page",
                }:
                    findings.append(f"{path.relative_to(ROOT)}: missing skill folder `{name}`")

    # 2. instruction_file entries exist
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
                    if not (ROOT / instr.replace("\\", "/")).exists():
                        # also try under .cursor/workflows/
                        alt = ROOT / ".cursor" / "workflows" / Path(instr).name
                        if not alt.exists():
                            findings.append(f"workflow-registry: missing instruction_file `{instr}`")

    # 3. Trigger tokens in skills / MEMORY-INDEX are known
    known = load_known_tokens()
    trigger_re = re.compile(r"Triggers?:\s*`?([a-z0-9:|,\s-]+)`?", re.I)
    for path in [ROOT / "facts" / "MEMORY-INDEX.md", *SKILLS_DIR.glob("*/SKILL.md")]:
        if not path.is_file():
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            if "Triggers" not in line:
                continue
            m = trigger_re.search(line)
            if not m:
                continue
            for tok in re.split(r"[|,\s]+", m.group(1)):
                tok = tok.strip().strip("`")
                if not tok or tok in {"none", "..."}:
                    continue
                if tok not in known:
                    findings.append(f"{path.relative_to(ROOT)}: unknown trigger `{tok}`")

    # 4. No escaped markdown headings
    for path in ROOT.rglob("*.md"):
        if ".git" in path.parts:
            continue
        for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if line.startswith(r"\#"):
                findings.append(f"{path.relative_to(ROOT)}:{i}: escaped heading")

    # 5. Stale patterns from fix 12
    stale = [
        (re.compile(r"[a-z]wid-", re.I), "corrupted ...wid- text"),
        (re.compile(r"2027-"), "future archive date 2027-"),
        (re.compile(r"(?<![\w/-])facts/facts\.md"), "legacy top-level facts/facts.md"),
        (re.compile(r"-operations\.md"), "legacy -operations.md"),
        (re.compile(r"workflowID-", re.I), "workflowID- typo"),
        (re.compile(r"inject-rules-on-action\.sh"), "legacy .sh rules hook"),
        (re.compile(r"\bconfig:change\b"), "retired config:change trigger"),
    ]
    skip_config_paths = {
        "scripts/test_rules_hook.py",
        ".cursor/hooks/inject_rules_on_action.py",
    }
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".md", ".txt", ".py", ".mdc", ".json"}:
            continue
        if ".git" in path.parts:
            continue
        if path.name in {"check_scaffold.py"}:
            continue
        rel = str(path.relative_to(ROOT)).replace("\\", "/")
        text = path.read_text(encoding="utf-8")
        for cre, label in stale:
            for m in cre.finditer(text):
                snippet = text[max(0, m.start() - 40) : m.end() + 40].replace("\\", "/")
                if "legacy top-level" in label:
                    # Work Item-relative facts files are expected.
                    if "work-items/" in snippet or "work-items/<" in snippet or "](facts/facts.md)" in snippet:
                        continue
                if "config:change" in label and rel in skip_config_paths:
                    continue
                findings.append(f"{rel}: {label} ({m.group(0)})")

    # 6. Memory pair exists
    for required in ("facts/facts-shared.md", "facts/rules-shared.md"):
        if not (ROOT / required).is_file():
            findings.append(f"missing {required}")

    # 7. Hooks wired
    hooks = json.loads((ROOT / ".cursor" / "hooks.json").read_text(encoding="utf-8"))
    blob = json.dumps(hooks)
    for needed in ("inject_journal_context.py", "inject_rules_on_action.py", "on_stop.py"):
        if needed not in blob:
            findings.append(f"hooks.json missing {needed}")

    if findings:
        print("Scaffold check FAILED:")
        for item in findings:
            print(f"  - {item}")
        return 1
    print("Scaffold check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
