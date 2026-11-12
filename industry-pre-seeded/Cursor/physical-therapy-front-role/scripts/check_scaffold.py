#!/usr/bin/env python3
"""Integrity check for this Cursor expert scaffold. Exit non-zero on findings."""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME = re.compile(r"(?:run\s+|skill\s+|invoke\s+)?`?([a-z][a-z0-9-]{2,})`?", re.I)
BACKTICK_PATH = re.compile(r"`([^`]+)`")
PLACEHOLDER = re.compile(r"<(?:id|WID|work-item-id|context_id|node|node-id|label|task-id)[^>]*>", re.I)
ESCAPED_HEADING = re.compile(r"^\\#", re.M)
BAD_PATTERNS = [
    (re.compile(r"[a-z]wid-", re.I), "folloWID-style corruption ([a-z]wid-)"),
    (re.compile(r"2027-"), "future date 2027-"),
    (re.compile(r"(?<![/\w-])facts/facts\.md"), "top-level facts/facts.md"),
    (re.compile(r"workflowID-", re.I), "workflowID- typo"),
    (re.compile(r"config:change"), "retired trigger config:change"),
]

ALLOW_MISSING = {
    ".cursor/role-skills.md",
    ".cursor/active-work-item.txt",
    ".cursor/active-qa-session.txt",
    ".cursor/plans/",
    "docs/design/hld.md",
    "docs/design/dd.md",
    "docs/design/requirements-summary.md",
    "docs/diagrams/",
    "docs/diagrams/index.html",
    "docs/decisions/",
    "docs/incident/assessment.md",
}

# Skills this PT role actually requires (from AGENTS.md / MyRole). Leftover
# developer skill folders may exist; they are not required to be referenced.
REQUIRED_SKILL_HINTS = {
    "continue",
    "define-role",
    "journal-keeper",
    "remember",
    "promote-facts-rules",
    "workflow-selector",
    "switch-context",
    "operator-qa",
    "integrate-docs",
    "memory-optimize",
}


def _load_known_tokens() -> set[str]:
    hook = ROOT / ".cursor" / "hooks" / "inject_rules_on_action.py"
    spec = importlib.util.spec_from_file_location("inject_rules_on_action", hook)
    if spec is None or spec.loader is None:
        return set()
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return set(getattr(mod, "KNOWN_TOKENS", []) or [])


def _skills_on_disk() -> set[str]:
    base = ROOT / ".cursor" / "skills"
    if not base.is_dir():
        return set()
    return {p.name for p in base.iterdir() if p.is_dir()}


def _iter_docs() -> list[Path]:
    paths: list[Path] = []
    for rel in [
        "AGENTS.md",
        "MyRole.txt",
        "README.md",
        "QUICK-START.md",
        ".cursor/CONTEXT-SYSTEM.md",
    ]:
        p = ROOT / rel
        if p.is_file():
            paths.append(p)
    for folder in [
        ROOT / ".cursor" / "skills",
        ROOT / ".cursor" / "workflows",
        ROOT / "facts",
    ]:
        if folder.is_dir():
            paths.extend(folder.rglob("*.md"))
    return paths


def _path_exists(raw: str) -> bool:
    text = raw.strip().rstrip("/")
    if not text or "://" in text or text.startswith("work-item:"):
        return True
    if "<" in text or ">" in text:
        # Runtime / template placeholders (workflow-type, name, id, …)
        return True
    if any(text.startswith(a.rstrip("/")) or text == a.rstrip("/") for a in ALLOW_MISSING):
        return True
    if text in {"facts/facts.md", "facts/rules.md"}:
        # Mentions of archived single-file memory; Work Item copies use work-items/.../facts/
        return True
    if text.startswith("docs/tools/") and "<" in text:
        return True
    if PLACEHOLDER.search(text):
        candidate = PLACEHOLDER.sub("_TEMPLATE", text)
        path = ROOT / candidate
        if path.exists():
            return True
        parts = Path(candidate).parts
        if "_TEMPLATE" in parts:
            return (ROOT / Path(*parts[: parts.index("_TEMPLATE") + 1])).exists()
        return True
    path = ROOT / text
    if path.exists():
        return True
    if (ROOT / ".cursor" / "skills" / text).is_dir():
        return True
    if (ROOT / ".cursor" / "workflows" / f"{text}.md").is_file():
        return True
    return False


def main() -> int:
    findings: list[str] = []
    on_disk = _skills_on_disk()
    for name in sorted(REQUIRED_SKILL_HINTS):
        if name not in on_disk:
            findings.append(f"missing required skill folder: {name}")

    # Named skills in AGENTS.md that look like skill folders
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8") if (ROOT / "AGENTS.md").is_file() else ""
    for match in re.finditer(r"\*\*([a-z][a-z0-9-]{2,})\*\*", agents):
        name = match.group(1)
        if name in {"physical", "therapy"}:
            continue
        skill_dir = ROOT / ".cursor" / "skills" / name
        if name in REQUIRED_SKILL_HINTS and not skill_dir.is_dir():
            findings.append(f"AGENTS.md names missing skill: {name}")

    # Registry instruction files
    registry = ROOT / ".cursor" / "workflows" / "workflow-registry.json"
    if registry.is_file():
        try:
            data = json.loads(registry.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            findings.append(f"workflow-registry.json invalid: {exc}")
            data = {}
        workflows = data.get("workflows") if isinstance(data, dict) else None
        if isinstance(workflows, list):
            for entry in workflows:
                if not isinstance(entry, dict):
                    continue
                instr = entry.get("instruction_file") or entry.get("file")
                if isinstance(instr, str) and instr.strip():
                    if not (ROOT / instr).is_file():
                        findings.append(f"missing instruction_file: {instr}")

    known = _load_known_tokens()
    trigger_re = re.compile(r"\b(write:[a-z0-9:-]+|git:[a-z0-9:-]+|pr:[a-z0-9:-]+|sql:[a-z0-9:-]+|config:[a-z0-9:-]+)\b")
    for path in _iter_docs():
        text = path.read_text(encoding="utf-8")
        rel = str(path.relative_to(ROOT)).replace("\\", "/")
        if ESCAPED_HEADING.search(text):
            findings.append(f"escaped heading in {rel}")
        for pattern, label in BAD_PATTERNS:
            if pattern.search(text) and "check_scaffold.py" not in rel:
                if "facts/facts.md" in label:
                    # Flag only bare top-level mentions, not work-items/.../facts/facts.md
                    if "work-items/" in text and "facts/facts.md" in text:
                        # Still scan line-by-line for bare mentions
                        bare = False
                        for line in text.splitlines():
                            if "facts/facts.md" in line and "work-items/" not in line:
                                bare = True
                                break
                        if not bare:
                            continue
                    elif "work-items/" in rel:
                        continue
                findings.append(f"{label} in {rel}")
        if path.suffix == ".md" and known:
            for tok in trigger_re.findall(text):
                if tok.endswith((":doc", ":csv", ":sql", ":push", ":commit", ":open", ":generate", ":change")):
                    if tok not in known and tok != "none" and "TRIGGER-INDEX" not in rel:
                        # vocabulary docs may list tokens; only flag unknown non-role tokens that look actionable
                        if tok.startswith(("git:", "pr:", "sql:", "config:")):
                            findings.append(f"unknown trigger `{tok}` in {rel}")

        if path.name in {"AGENTS.md", "README.md", "QUICK-START.md", "MyRole.txt"} or ".cursor/skills" in rel:
            for raw in BACKTICK_PATH.findall(text):
                if "/" not in raw and "\\" not in raw:
                    continue
                if raw.startswith(("http", "gh ", "git ", "py ", "python")):
                    continue
                if any(ch in raw for ch in ["*", "(", ")", " "]):
                    continue
                if not _path_exists(raw.replace("\\", "/")):
                    # soften: only report clear scaffold paths
                    if raw.startswith((".cursor/", "facts/", "journals/", "work-items/", "scripts/", "docs/")):
                        findings.append(f"missing path `{raw}` in {rel}")

    readme = ROOT / "README.md"
    quick = ROOT / "QUICK-START.md"
    if readme.is_file() and quick.is_file():
        if readme.read_text(encoding="utf-8") != quick.read_text(encoding="utf-8"):
            # This role keeps them as different short guides — warn, do not fail hard unless identical was promised
            findings.append("README.md and QUICK-START.md differ (expected for this role; keep both intentional)")

    # Fail only on real problems; demote the README differ to stderr note
    hard = [f for f in findings if not f.startswith("README.md and QUICK-START.md differ")]
    note = [f for f in findings if f.startswith("README.md and QUICK-START.md differ")]
    for item in note:
        print(f"NOTE: {item}")
    if hard:
        print("FAIL:")
        for item in hard:
            print(f"  - {item}")
        return 1
    print("check_scaffold: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
