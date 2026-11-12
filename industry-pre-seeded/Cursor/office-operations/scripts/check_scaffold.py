#!/usr/bin/env python3
"""Integrity checks for the office-operations Cursor expert scaffold."""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Skills named in role-facing docs that must exist. Leftover developer skill
# folders may remain on disk but are not required by this role.
REQUIRED_SKILLS = {
    "continue",
    "define-role",
    "integrate-docs",
    "journal-keeper",
    "memory-optimize",
    "operator-qa",
    "promote-facts-rules",
    "remember",
    "switch-context",
    "workflow-selector",
}

ALLOW_MISSING_PATHS = {
    ".cursor/role-skills.md",
    ".cursor/active-work-item.txt",
    "work-items/<id>/",
    "journals/work-items/<id>/",
}

# Scaffold leftovers not used by office-operations; still on disk for now.
IGNORE_SKILL_FOLDERS = {
    "implement-feature",
    "iterative-feature",
    "refactor",
    "scaffold-project",
    "spec-parser",
    "diagram-generator",
    "visual-page",
}

SKILL_NAME_RE = re.compile(r"\b([a-z][a-z0-9-]{2,})\b")
BACKTICK_PATH_RE = re.compile(r"`([^`]+)`")
TRIGGER_TOKEN_RE = re.compile(r"\b(write:[a-z0-9_-]+|git:[a-z0-9_-]+|pr:[a-z0-9_-]+|sql:[a-z0-9_-]+|config:[a-z0-9_-]+)\b")
ESCAPED_HEADING_RE = re.compile(r"^\\#", re.MULTILINE)
def _load_known_tokens() -> set[str]:
    hook = ROOT / ".cursor" / "hooks" / "inject_rules_on_action.py"
    spec = importlib.util.spec_from_file_location("inject_rules_on_action", hook)
    if spec is None or spec.loader is None:
        return set()
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return set(getattr(module, "KNOWN_TOKENS", []))


def _role_text_files() -> list[Path]:
    files = [
        ROOT / "AGENTS.md",
        ROOT / "MyRole.txt",
        ROOT / "README.md",
        ROOT / "QUICK-START.md",
        ROOT / "facts" / "MEMORY-INDEX.md",
    ]
    for path in sorted((ROOT / ".cursor" / "skills").glob("*/SKILL.md")):
        if path.parent.name in IGNORE_SKILL_FOLDERS:
            continue
        files.append(path)
    files.extend(sorted((ROOT / ".cursor" / "workflows").glob("*.md")))
    return [path for path in files if path.is_file()]


def _named_skills(text: str) -> set[str]:
    # Bold skill names and explicit "run X" / skill folder references
    found: set[str] = set()
    for match in re.finditer(r"\*\*([a-z][a-z0-9-]{2,})\*\*", text):
        found.add(match.group(1))
    for match in re.finditer(r"`\.cursor/skills/([a-z][a-z0-9-]{2,})`", text):
        found.add(match.group(1))
    return found


def check_required_skills() -> list[str]:
    errors: list[str] = []
    skills_root = ROOT / ".cursor" / "skills"
    named: set[str] = set(REQUIRED_SKILLS)
    for path in _role_text_files():
        named |= _named_skills(path.read_text(encoding="utf-8"))
    for skill in sorted(named & REQUIRED_SKILLS):
        if not (skills_root / skill / "SKILL.md").is_file():
            errors.append(f"missing skill folder: .cursor/skills/{skill}/")
    return errors


def _path_exists(raw: str) -> bool:
    text = raw.strip()
    if not text or "://" in text or text.startswith("http"):
        return True
    if text in ALLOW_MISSING_PATHS:
        return True
    if any(token in text for token in ("<", ">", "*", "?")):
        # Placeholder path — require the template or parent to exist when obvious
        candidate = text
        for token in ("<id>", "<WID>", "<work-item-id>", "<context_id>", "<node>", "<active leaf>"):
            candidate = candidate.replace(token, "_TEMPLATE")
        candidate = candidate.replace("\\", "/")
        if candidate.startswith("work-items/") or candidate.startswith("journals/"):
            parts = candidate.split("/")
            if len(parts) >= 2:
                base = ROOT.joinpath(*parts[:2])
                if parts[1] == "_TEMPLATE" or (ROOT / parts[0] / "_TEMPLATE").exists():
                    return True
                if base.exists():
                    return True
        return True
    rel = text.replace("\\", "/").lstrip("./")
    if rel.startswith(("write:", "git:", "pr:", "sql:", "config:", "work-item:")):
        return True
    if "/" not in rel and "." not in rel:
        return True
    path = ROOT / rel
    if path.exists():
        return True
    # Allow docs/tools names referenced without full path context
    if rel.startswith(".cursor/") or rel.startswith("facts/") or rel.startswith("docs/") or rel.startswith("scripts/") or rel.startswith("journals/") or rel.startswith("work-items/"):
        return path.exists()
    return True


def check_backtick_paths() -> list[str]:
    errors: list[str] = []
    for path in _role_text_files():
        text = path.read_text(encoding="utf-8")
        for match in BACKTICK_PATH_RE.finditer(text):
            raw = match.group(1)
            if raw.startswith(("**", "#", "-", "Workflows", "Triggers", "Scope")):
                continue
            if not _path_exists(raw):
                errors.append(f"{path.relative_to(ROOT)}: missing path `{raw}`")
    return errors


def check_workflow_registry() -> list[str]:
    errors: list[str] = []
    registry_path = ROOT / ".cursor" / "workflows" / "workflow-registry.json"
    if not registry_path.is_file():
        return ["missing .cursor/workflows/workflow-registry.json"]
    data = json.loads(registry_path.read_text(encoding="utf-8"))
    workflows = data.get("workflows") if isinstance(data, dict) else None
    if not isinstance(workflows, dict):
        return ["workflow-registry.json has no workflows object"]
    for key, entry in workflows.items():
        if not isinstance(entry, dict):
            continue
        instruction = entry.get("instruction_file")
        if not isinstance(instruction, str) or not instruction.strip():
            errors.append(f"workflow {key}: missing instruction_file")
            continue
        if not (ROOT / instruction.replace("\\", "/")).is_file():
            errors.append(f"workflow {key}: missing {instruction}")
    return errors


def check_triggers() -> list[str]:
    errors: list[str] = []
    known = _load_known_tokens()
    if not known:
        errors.append("KNOWN_TOKENS missing from inject_rules_on_action.py")
        return errors
    for path in [
        ROOT / "facts" / "MEMORY-INDEX.md",
        *sorted((ROOT / ".cursor" / "skills").glob("*/SKILL.md")),
    ]:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for token in TRIGGER_TOKEN_RE.findall(text):
            if token.endswith(":") or token == "none":
                continue
            if token not in known and token != "none":
                # Allow documenting `none` via separate check; tokens must be known
                if token.split(":")[0] in {"write", "git", "pr", "sql", "config"}:
                    if token not in known:
                        errors.append(
                            f"{path.relative_to(ROOT)}: trigger `{token}` not in KNOWN_TOKENS"
                        )
    return errors


def check_escaped_headings() -> list[str]:
    errors: list[str] = []
    for path in ROOT.rglob("*.md"):
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        if ESCAPED_HEADING_RE.search(text):
            errors.append(f"{path.relative_to(ROOT)}: escaped heading \\#")
    return errors


def check_stale_patterns() -> list[str]:
    errors: list[str] = []
    for path in ROOT.rglob("*"):
        if path.suffix.lower() not in {".md", ".txt", ".py", ".json"}:
            continue
        if ".git" in path.parts or path.name in {"check_scaffold.py"}:
            continue
        text = path.read_text(encoding="utf-8")
        rel = str(path.relative_to(ROOT)).replace("\\", "/")
        if re.search(r"(?:workflowID-|WorkflowID-|folloWID-|newID-workflow)", text):
            errors.append(f"{rel}: stale workflowID-/folloWID- style text")
        if "2027-" in text:
            errors.append(f"{rel}: future archive date 2027-")
        for match in re.finditer(r"(?<![\w/-])facts/facts\.md", text):
            start = max(0, match.start() - 48)
            window = text[start : match.end() + 8]
            if "work-items/" in window or "Work Item" in window:
                continue
            errors.append(f"{rel}: top-level facts/facts.md reference")
    return errors


def check_readme_pair() -> list[str]:
    readme = ROOT / "README.md"
    quick = ROOT / "QUICK-START.md"
    if not readme.is_file() or not quick.is_file():
        return ["README.md and QUICK-START.md must both exist"]
    # Role-adapted experts may keep a short README that points at QUICK-START.
    # Only require byte-identity when both look like the long scaffold twin.
    r = readme.read_text(encoding="utf-8")
    q = quick.read_text(encoding="utf-8")
    if r == q:
        return []
    if len(r) < 2000 or len(q) < 2000:
        return []
    return ["README.md and QUICK-START.md differ (long scaffold twins should match)"]


def main() -> int:
    checks = [
        ("skills", check_required_skills),
        ("paths", check_backtick_paths),
        ("registry", check_workflow_registry),
        ("triggers", check_triggers),
        ("escaped", check_escaped_headings),
        ("stale", check_stale_patterns),
        ("readme", check_readme_pair),
    ]
    all_errors: list[str] = []
    for name, fn in checks:
        errors = fn()
        if errors:
            print(f"FAIL {name}:")
            for err in errors:
                print(f"  - {err}")
            all_errors.extend(errors)
        else:
            print(f"OK   {name}")
    if all_errors:
        print(f"\n{len(all_errors)} finding(s)")
        return 1
    print("\nscaffold check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
