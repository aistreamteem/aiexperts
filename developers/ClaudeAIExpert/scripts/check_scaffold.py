#!/usr/bin/env python3
"""Integrity check for the expert scaffold. Exit non-zero on any finding."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / ".claude" / "skills"
WORKFLOWS_DIR = ROOT / ".claude" / "workflows"
REGISTRY = WORKFLOWS_DIR / "workflow-registry.json"

DOC_GLOBS = [
    "CLAUDE.md",
    "MyRole.txt",
    "README.md",
    "QUICK-START.md",
    ".claude/**/*.md",
    "facts/*.md",
    "docs/**/*.md",
]

ALLOW_MISSING = {
    ".claude/active-context.txt",
    ".claude/active-work-item.txt",
    ".claude/active-qa-session.txt",
    ".claude/role-skills.md",
    "docs/role/role-definition.md",
}

# Runtime / work-item artifact prefixes that are created during a pipeline, not shipped.
RUNTIME_PREFIXES = (
    "docs/design/",
    "docs/diagrams/",
    "docs/decisions/",
    "docs/features/",
    "docs/incident/",
    "docs/role/",
    "work-items/<",
    "journals/work-items/<",
    "qa-sessions/<",
    "qa-sessions/Q",
    ".claude/workflows/<",
    "facts/facts-<",
    "facts/rules-<",
)

PLACEHOLDER = re.compile(
    r"<(?:id|WID|work-item-id|context_id|feature-id|node|label|task-id|workflow-type|workflow)[^>]*>",
    re.I,
)
BACKTICK_PATH = re.compile(r"`([^`]+)`")
SKILL_NAME = re.compile(r"(?:run\s+)?([a-z][a-z0-9-]{2,})(?:\s*\(|\s+skill|\s*$)", re.I)
ESCAPED_HEADING = re.compile(r"^\\#")
BAD_PATTERNS = [
    (re.compile(r"workflowID-", re.I), "workflowID- typo"),
    (re.compile(r"folloWID", re.I), "folloWID typo"),
    (re.compile(r"2027-"), "future archive date 2027-"),
    (re.compile(r"facts/(?:facts|rules)-operations\.md"), "operations memory file"),
    (re.compile(r"config:change"), "retired trigger config:change"),
]


def _fail(findings: list[str], message: str) -> None:
    findings.append(message)


def _iter_docs() -> list[Path]:
    files: set[Path] = set()
    for pattern in DOC_GLOBS:
        files.update(ROOT.glob(pattern))
    return sorted(p for p in files if p.is_file())


def _skill_names_referenced(text: str) -> set[str]:
    known_dirs = {p.name for p in SKILLS_DIR.iterdir() if p.is_dir()}
    # Also accept names the scaffold is expected to mention even before folders exist
    # during partial repairs — here we only collect explicit skill-folder references.
    found: set[str] = set()
    for match in re.finditer(r"`?\.claude/skills/([a-z0-9-]+)", text):
        found.add(match.group(1))
    for match in re.finditer(r"\*\*([a-z0-9-]+)\*\*", text):
        name = match.group(1)
        if name in known_dirs or name in {
            "hld-writer",
            "dd-writer",
            "task-breakdown",
            "git-workflow",
            "spec-parser",
            "scaffold-project",
            "implement-feature",
            "diagram-generator",
            "journal-keeper",
            "continue",
            "define-role",
            "workflow-selector",
            "remember",
            "promote-facts-rules",
            "integrate-docs",
            "memory-optimize",
            "iterative-feature",
            "refactor",
            "switch-context",
            "operator-qa",
            "visual-page",
        }:
            found.add(name)
    for match in re.finditer(r"(?:run|use)\s+(?:the\s+)?([a-z][a-z0-9-]{2,})", text):
        name = match.group(1)
        if name in {
            "hld-writer",
            "dd-writer",
            "task-breakdown",
            "git-workflow",
            "spec-parser",
            "scaffold-project",
            "implement-feature",
            "diagram-generator",
            "journal-keeper",
            "continue",
            "define-role",
            "workflow-selector",
            "remember",
            "promote-facts-rules",
            "integrate-docs",
            "memory-optimize",
            "iterative-feature",
            "refactor",
            "switch-context",
            "operator-qa",
            "visual-page",
            "test-writer",
        }:
            found.add(name)
    return found


def check_skills(findings: list[str]) -> None:
    required: set[str] = set()
    for path in _iter_docs():
        text = path.read_text(encoding="utf-8", errors="replace")
        required |= _skill_names_referenced(text)
    # Always require the phase skills named by the developer pipeline.
    required |= {
        "hld-writer",
        "dd-writer",
        "task-breakdown",
        "git-workflow",
        "spec-parser",
        "scaffold-project",
        "implement-feature",
        "diagram-generator",
        "journal-keeper",
        "continue",
        "define-role",
        "workflow-selector",
        "remember",
        "promote-facts-rules",
        "integrate-docs",
        "memory-optimize",
        "iterative-feature",
        "refactor",
        "switch-context",
        "operator-qa",
    }
    for name in sorted(required):
        if name == "test-writer":
            _fail(findings, "obsolete skill referenced: test-writer")
            continue
        if not (SKILLS_DIR / name / "SKILL.md").is_file():
            _fail(findings, f"missing skill folder: .claude/skills/{name}/SKILL.md")


def check_registry(findings: list[str]) -> None:
    if not REGISTRY.is_file():
        _fail(findings, "missing workflow-registry.json")
        return
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    workflows = data.get("workflows") if isinstance(data, dict) else None
    if not isinstance(workflows, dict):
        _fail(findings, "workflow-registry.json has no workflows map")
        return
    for key, meta in workflows.items():
        if not isinstance(meta, dict):
            continue
        rel = str(meta.get("instruction_file") or "")
        if not rel:
            _fail(findings, f"workflow {key} missing instruction_file")
            continue
        path = ROOT / rel
        if not path.is_file():
            _fail(findings, f"workflow instruction missing: {rel}")


def _path_exists(raw: str) -> bool:
    text = raw.strip()
    if not text or "://" in text or text.startswith("http"):
        return True
    if text in ALLOW_MISSING:
        return True
    # Skip non-path-looking tokens
    if " " in text and not text.startswith(".") and "/" not in text and "\\" not in text:
        return True
    if not any(ch in text for ch in "/\\.") and not text.endswith(".md"):
        return True
    normalized = text.replace("\\", "/")
    if any(normalized.startswith(prefix) for prefix in RUNTIME_PREFIXES):
        return True
    if PLACEHOLDER.search(normalized):
        # Treat placeholders as template wildcards against known roots.
        if normalized.startswith("work-items/"):
            return (ROOT / "work-items" / "_TEMPLATE").is_dir()
        if normalized.startswith("journals/work-items/"):
            return (ROOT / "journals" / "work-items" / "_TEMPLATE").is_dir()
        if normalized.startswith("qa-sessions/"):
            return (ROOT / "qa-sessions" / "_TEMPLATE").is_dir()
        if normalized.startswith("facts/"):
            return (ROOT / "facts").is_dir()
        if normalized.startswith(".claude/skills/"):
            return SKILLS_DIR.is_dir()
        if normalized.startswith(".claude/workflows/"):
            return WORKFLOWS_DIR.is_dir()
        if normalized.startswith("docs/"):
            return True
        return True
    candidate = ROOT / normalized
    if candidate.exists():
        return True
    # Allow paths that are clearly runtime outputs under a work item.
    if normalized.startswith("work-items/") and "/docs/" in normalized:
        return True
    if normalized.startswith("work-items/") and normalized.endswith(
        ("TODOS.md", "STATUS.md", "NEEDS-ATTENTION.md")
    ):
        return True
    # Bare docs/* paths in skills mean work-item-relative runtime artifacts.
    if normalized.startswith("docs/") and normalized.endswith(
        (".md", ".mmd", ".html", ".json")
    ):
        return True
    return False


def check_backtick_paths(findings: list[str]) -> None:
    interesting = re.compile(
        r"^(?:\.claude/|journals/|work-items/|facts/|docs/|scripts/|MyRole\.txt|CLAUDE\.md|README\.md|QUICK-START\.md)"
    )
    for path in _iter_docs():
        text = path.read_text(encoding="utf-8", errors="replace")
        for match in BACKTICK_PATH.finditer(text):
            raw = match.group(1).strip()
            if not interesting.match(raw.replace("\\", "/")):
                continue
            if raw.endswith("/") or raw.endswith("/*") or "*" in raw:
                continue
            if not _path_exists(raw):
                rel = path.relative_to(ROOT).as_posix()
                _fail(findings, f"missing path `{raw}` referenced from {rel}")


def check_triggers(findings: list[str]) -> None:
    sys.path.insert(0, str(ROOT / ".claude" / "hooks"))
    try:
        from inject_rules_on_action import KNOWN_TOKENS  # type: ignore
    except Exception as exc:  # noqa: BLE001
        _fail(findings, f"cannot import KNOWN_TOKENS: {exc}")
        return
    known = set(KNOWN_TOKENS) | {"none"}
    token_re = re.compile(
        r"\b(?:write|sql|git|pr|config):[a-z0-9-]+\b"
    )
    for path in [
        ROOT / ".claude" / "skills" / "remember" / "SKILL.md",
        ROOT / ".claude" / "skills" / "promote-facts-rules" / "SKILL.md",
        ROOT / "facts" / "MEMORY-INDEX.md",
    ]:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for token in set(token_re.findall(text)):
            # findall with one group returns groups; rework:
            pass
        for match in token_re.finditer(text):
            token = match.group(0)
            if token not in known:
                _fail(findings, f"unknown trigger `{token}` in {path.relative_to(ROOT).as_posix()}")


def check_markdown_hygiene(findings: list[str]) -> None:
    for path in _iter_docs():
        text = path.read_text(encoding="utf-8", errors="replace")
        rel = path.relative_to(ROOT).as_posix()
        for i, line in enumerate(text.splitlines(), 1):
            if ESCAPED_HEADING.match(line):
                _fail(findings, f"escaped heading in {rel}:{i}")
            for pattern, label in BAD_PATTERNS:
                if pattern.search(line):
                    # Allow documenting banned patterns only inside check_scaffold itself.
                    if path.name == "check_scaffold.py":
                        continue
                    _fail(findings, f"{label} in {rel}:{i}")


def check_readme_pair(findings: list[str]) -> None:
    readme = ROOT / "README.md"
    quick = ROOT / "QUICK-START.md"
    if not readme.is_file() or not quick.is_file():
        return
    quick_text = quick.read_text(encoding="utf-8", errors="replace").strip()
    # Allow a one-line pointer, or full identity with README.
    if quick_text == readme.read_text(encoding="utf-8", errors="replace").strip():
        return
    if "README.md" in quick_text and len(quick_text.splitlines()) <= 5:
        return
    _fail(findings, "README.md and QUICK-START.md differ; keep them identical or make QUICK-START a pointer")


def check_no_legacy_journal_writes(findings: list[str]) -> None:
    pattern = re.compile(r"work-items/.+/journal/")
    for path in _iter_docs():
        text = path.read_text(encoding="utf-8", errors="replace")
        rel = path.relative_to(ROOT).as_posix()
        for i, line in enumerate(text.splitlines(), 1):
            if "Do not write" in line or "pointer" in line.lower():
                continue
            if pattern.search(line) and "legacy" not in line.lower():
                # Still flag instructional write targets.
                if any(word in line.lower() for word in ("write", "update", "journal:", "read ")):
                    if "journals/work-items" in line:
                        continue
                    _fail(findings, f"legacy journal path in {rel}:{i}")


def main() -> int:
    findings: list[str] = []
    check_skills(findings)
    check_registry(findings)
    check_backtick_paths(findings)
    check_triggers(findings)
    check_markdown_hygiene(findings)
    check_readme_pair(findings)
    check_no_legacy_journal_writes(findings)

    if findings:
        print(f"scaffold check FAILED ({len(findings)} finding(s)):")
        for item in findings:
            print(f"  - {item}")
        return 1
    print("scaffold check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
