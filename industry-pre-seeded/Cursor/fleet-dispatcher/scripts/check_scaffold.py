#!/usr/bin/env python3
"""Integrity check for this Cursor role expert scaffold."""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALLOW_MISSING = {
    ".cursor/role-skills.md",
    ".cursor/plans/",
    "work-items/<id>/",
    "journals/work-items/<id>/",
}

SKILL_NAME_RE = re.compile(r"`([a-z][a-z0-9-]{1,40})`")
PATH_RE = re.compile(
    r"`((?:\.cursor|facts|journals|work-items|docs|scripts|qa-sessions)/[^`\n]+)`"
)


def _load_known_tokens() -> set[str]:
    hook = ROOT / ".cursor" / "hooks" / "inject_rules_on_action.py"
    spec = importlib.util.spec_from_file_location("rules_hook", hook)
    if spec is None or spec.loader is None:
        return set()
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return set(getattr(mod, "KNOWN_TOKENS", []) or [])


def _skill_dirs() -> set[str]:
    skills = ROOT / ".cursor" / "skills"
    return {p.name for p in skills.iterdir() if p.is_dir()} if skills.is_dir() else set()


def _canonical_skills() -> set[str]:
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    names = set()
    for line in agents.splitlines():
        if "Canonical expert skills:" in line:
            names.update(SKILL_NAME_RE.findall(line))
    return names


def _expand_placeholder(path: str) -> bool:
    if any(path.startswith(a) or path == a.rstrip("/") for a in ALLOW_MISSING):
        return True
    # Treat <id>, <WID>, <context_id>, <work-item-id> as template wildcards
    if re.search(r"<[^>]+>", path):
        candidate = re.sub(r"<[^>]+>", "_TEMPLATE", path)
        if (ROOT / candidate).exists():
            return True
        # journals/work-items/<id>/progress.md → template progress
        parts = path.replace("\\", "/").split("/")
        rebuilt = []
        for part in parts:
            if part.startswith("<") and part.endswith(">"):
                rebuilt.append("_TEMPLATE")
            else:
                rebuilt.append(part)
        return (ROOT / "/".join(rebuilt)).exists()
    return (ROOT / path).exists()


def main() -> int:
    findings: list[str] = []
    skill_dirs = _skill_dirs()
    for name in sorted(_canonical_skills()):
        if name not in skill_dirs:
            findings.append(f"missing skill folder for canonical skill `{name}`")

    docs = []
    for pattern in ("AGENTS.md", "MyRole.txt", "README.md", "QUICK-START.md",
                    ".cursor/**/*.md", ".cursor/workflows/*.md", "docs/**/*.md"):
        docs.extend(ROOT.glob(pattern))
    seen_paths: set[str] = set()
    for doc in docs:
        if not doc.is_file():
            continue
        text = doc.read_text(encoding="utf-8", errors="replace")
        rel = doc.relative_to(ROOT).as_posix()
        if rel.startswith("facts/TRIGGER-INDEX"):
            continue
        for match in PATH_RE.findall(text):
            path = match.strip().rstrip(").,;")
            if path in seen_paths:
                continue
            seen_paths.add(path)
            if path.endswith(".md") or path.endswith(".py") or path.endswith(".json") or path.endswith("/"):
                if not _expand_placeholder(path):
                    # Skip purely illustrative runtime paths
                    if "<" in path or path.endswith("/"):
                        continue
                    findings.append(f"missing path `{path}` referenced from {rel}")

        if re.search(r"^\\#", text, re.M):
            findings.append(f"escaped heading in {rel}")
        if re.search(r"[a-z]wid-", text, re.I) and "work-item" not in text.lower():
            # Narrow: workflowID- style corruption
            if re.search(r"workflowID-|folloWID-|newID-workflow", text):
                findings.append(f"ID-corruption token in {rel}")
        if "2027-" in text:
            findings.append(f"future date 2027- in {rel}")
        # Top-level facts/facts.md (not under work-items/) is stale for this scaffold
        for m in re.finditer(r"(?<![\w/-])facts/facts\.md", text):
            start = max(0, m.start() - 48)
            window = text[start:m.end() + 8]
            if "work-items/" in window or "<id>/facts" in window or "<root_path>/facts" in window:
                continue
            findings.append(f"stale facts/facts.md reference in {rel}")
            break

    registry = ROOT / ".cursor" / "workflows" / "workflow-registry.json"
    if registry.is_file():
        data = json.loads(registry.read_text(encoding="utf-8"))
        for key, entry in (data.get("workflows") or {}).items():
            instr = entry.get("instruction_file")
            if instr and not (ROOT / instr).is_file():
                findings.append(f"registry workflow `{key}` missing `{instr}`")

    known = _load_known_tokens()
    trigger_re = re.compile(r"\b(write:[a-z]+|sql:[a-z]+|git:[a-z]+|pr:[a-z]+|config:[a-z]+)\b")
    for doc in list((ROOT / ".cursor" / "skills").glob("*/SKILL.md")) + [
        ROOT / "facts" / "MEMORY-INDEX.md"
    ]:
        if not doc.is_file():
            continue
        for tok in trigger_re.findall(doc.read_text(encoding="utf-8")):
            if tok not in known and tok != "none":
                findings.append(
                    f"trigger `{tok}` in {doc.relative_to(ROOT).as_posix()} not in KNOWN_TOKENS"
                )

    readme = ROOT / "README.md"
    quick = ROOT / "QUICK-START.md"
    if readme.is_file() and quick.is_file():
        if readme.read_text(encoding="utf-8") != quick.read_text(encoding="utf-8"):
            findings.append("README.md and QUICK-START.md differ")

    if findings:
        print("check_scaffold FAILED:")
        for item in findings:
            print(" -", item)
        return 1
    print("check_scaffold OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
