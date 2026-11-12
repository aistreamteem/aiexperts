#!/usr/bin/env python3
"""Integrity check for this Claude role expert scaffold."""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

RUNTIME_ALLOW = {
    ".claude/active-work-item.txt",  # legacy read fallback
    ".claude/active-qa-session.txt",
    ".claude/role-skills.md",
    ".claude/plans",
    "facts/TRIGGER-INDEX.md",
    "facts/trigger-index.json",
}

ROOT_PREFIXES = (
    ".claude/",
    "facts/",
    "journals/",
    "work-items/",
    "qa-sessions/",
    "scripts/",
    "docs/",
    "MyRole.txt",
    "CLAUDE.md",
    "README.md",
    "QUICK-START.md",
)

SKILL_REF_RE = re.compile(
    r"(?:run\s+\*\*|invoke\s+\*\*|skill\s+\*\*|/\*\*|`\.claude/skills/)([a-z][a-z0-9-]{2,})",
    re.I,
)
PATH_RE = re.compile(r"`([^`\n]+)`")
ESCAPED_HEADING = re.compile(r"(?m)^\\#")
TRIGGER_RE = re.compile(r"\*\*Triggers:\*\*\s*([^\n]+)")
WID_TYPO_RE = re.compile(r"(?i)(?:workflow|new)ID-")


def _load_known_tokens() -> set[str]:
    hook = ROOT / ".claude" / "hooks" / "inject_rules_on_action.py"
    spec = importlib.util.spec_from_file_location("inject_rules_on_action", hook)
    if spec is None or spec.loader is None:
        return set()
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return set(getattr(module, "KNOWN_TOKENS", []))


def _skills_on_disk() -> set[str]:
    base = ROOT / ".claude" / "skills"
    if not base.is_dir():
        return set()
    return {p.name for p in base.iterdir() if p.is_dir()}


def _iter_docs() -> list[Path]:
    paths: list[Path] = []
    for rel in ("CLAUDE.md", "MyRole.txt", "README.md", "QUICK-START.md"):
        path = ROOT / rel
        if path.is_file():
            paths.append(path)
    for folder in (
        ROOT / ".claude" / "skills",
        ROOT / ".claude" / "workflows",
        ROOT / "facts",
        ROOT / "docs",
    ):
        if folder.is_dir():
            paths.extend(p for p in folder.rglob("*.md") if p.is_file())
    ctx = ROOT / ".claude" / "CONTEXT-SYSTEM.md"
    if ctx.is_file():
        paths.append(ctx)
    return paths


def _normalize_placeholder(path: str) -> str:
    text = path.replace("\\", "/")
    text = re.sub(r"<[^>]+>", "_TEMPLATE", text)
    text = text.replace("WID-XXXXXXXX", "_TEMPLATE")
    return text


def _is_repo_path(raw: str) -> bool:
    text = raw.strip().replace("\\", "/")
    if not text or " " in text or text.startswith("http"):
        return False
    if text.startswith("/") or re.match(r"^[A-Za-z]:/", text):
        return False
    return text.startswith(ROOT_PREFIXES) or text in ROOT_PREFIXES


def _path_exists(raw: str) -> bool:
    text = raw.strip().replace("\\", "/")
    if text in RUNTIME_ALLOW or any(text.startswith(a.rstrip("/") + "/") or text == a for a in RUNTIME_ALLOW):
        return True
    if "<" in text or "*" in text or "YYYY" in text or "…" in text:
        # Runtime/template path: require only that the first segment exists.
        first = text.split("/", 1)[0]
        return (ROOT / first).exists()
    # Example Work Item folders are created at runtime.
    if text.startswith("work-items/") and "/_TEMPLATE" not in text:
        return (ROOT / "work-items").is_dir()
    probe = _normalize_placeholder(text)
    return (ROOT / probe).exists()


def main() -> int:
    findings: list[str] = []
    on_disk = _skills_on_disk()

    agents = ROOT / "CLAUDE.md"
    if agents.is_file():
        text = agents.read_text(encoding="utf-8")
        for match in re.finditer(r"\*\*([a-z][a-z0-9-]{2,})\*\*", text):
            name = match.group(1)
            if name in {
                "describe-csv",
                "group-compare-bars",
                "histogram-pack",
                "missing-and-outliers",
                "refresh-from-new-export",
                "scatter-and-corr",
                "small-multiples",
                "time-series-line",
            }:
                continue
            if (ROOT / ".claude" / "skills" / name).is_dir():
                continue
            # Bold names in AGENTS that look like skills
            if name in {
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
            }:
                if name not in on_disk:
                    findings.append(f"CLAUDE.md names missing skill {name}")

    for path in _iter_docs():
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(ROOT)
        if ESCAPED_HEADING.search(text):
            findings.append(f"escaped heading in {rel}")
        if WID_TYPO_RE.search(text):
            findings.append(f"workflowID-typo pattern in {rel}")
        if "2027-" in text:
            findings.append(f"future 2027- date in {rel}")
        for match in PATH_RE.finditer(text):
            raw = match.group(1).strip()
            if not _is_repo_path(raw):
                continue
            if not _path_exists(raw):
                findings.append(f"missing path `{raw}` in {rel}")

    registry = ROOT / ".claude" / "workflows" / "workflow-registry.json"
    if registry.is_file():
        try:
            data = json.loads(registry.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            findings.append("workflow-registry.json is not valid JSON")
            data = {}
        workflows = data.get("workflows") if isinstance(data, dict) else None
        entries: list[dict] = []
        if isinstance(workflows, list):
            entries = [e for e in workflows if isinstance(e, dict)]
        elif isinstance(workflows, dict):
            entries = [e for e in workflows.values() if isinstance(e, dict)]
        for entry in entries:
            instr = entry.get("instruction_file") or entry.get("file") or entry.get("path")
            if isinstance(instr, str) and instr.strip():
                candidates = [
                    ROOT / instr,
                    ROOT / ".claude" / "workflows" / Path(instr).name,
                ]
                if not any(c.exists() for c in candidates):
                    findings.append(f"registry instruction missing: {instr}")

    known = _load_known_tokens()
    for path in (ROOT / "facts").glob("rules-*.md"):
        for match in TRIGGER_RE.finditer(path.read_text(encoding="utf-8")):
            for tok in re.split(r"[,\s]+", match.group(1)):
                tok = tok.strip().strip("`")
                if not tok or tok == "none" or "|" in tok:
                    continue
                if known and tok not in known:
                    findings.append(f"unknown trigger `{tok}` in {path.name}")

    readme = ROOT / "README.md"
    quick = ROOT / "QUICK-START.md"
    if readme.is_file() and quick.is_file():
        readme_text = readme.read_text(encoding="utf-8")
        quick_text = quick.read_text(encoding="utf-8")
        pointer = (
            "QUICK-START.md" in readme_text and len(readme_text) < 400
        ) or ("README.md" in quick_text and len(quick_text) < 400)
        if readme_text != quick_text and not pointer:
            findings.append("README.md and QUICK-START.md differ")

    unique: list[str] = []
    seen: set[str] = set()
    for item in findings:
        if item not in seen:
            seen.add(item)
            unique.append(item)

    if unique:
        print(f"check_scaffold: {len(unique)} finding(s)")
        for item in unique[:40]:
            print(f"  - {item}")
        if len(unique) > 40:
            print(f"  ... and {len(unique) - 40} more")
        return 1
    print("check_scaffold: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
