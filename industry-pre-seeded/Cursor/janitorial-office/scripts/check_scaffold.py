#!/usr/bin/env python3
"""Integrity check for this expert scaffold. Exit non-zero on any finding."""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALLOW_RUNTIME = {
    ".cursor/role-skills.md",
    ".cursor/active-context.txt",
    ".cursor/active-work-item.txt",
    ".cursor/active-qa-session.txt",
}
PLACEHOLDER = re.compile(r"<(?:id|WID|work-item-id|context_id|node|/[^>]+)>", re.I)
SKILL_NAME = re.compile(r"`([a-z0-9][a-z0-9-]*)`")
BACKTICK_PATH = re.compile(
    r"`((?:\.cursor|journals|work-items|facts|docs|scripts|qa-sessions|MyRole\.txt|AGENTS\.md|"
    r"README\.md|QUICK-START\.md|DESIGN\.md)[^`]*)`"
)
BAD_PATTERNS = [
    (re.compile(r"(?i)[a-z]wid-"), "stale workflowID-/folloWID- style token"),
    (re.compile(r"2027-"), "future 2027- date leftover"),
    (re.compile(r"(?<!work-items/<id>/)facts/facts\.md"), "top-level facts/facts.md reference"),
    (re.compile(r"-operations\.md"), None),  # handled specially
    (re.compile(r"^\\#", re.M), "escaped markdown heading"),
]


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
    return {p.name for p in base.iterdir() if p.is_dir() and (p / "SKILL.md").is_file()}


def _named_skills() -> set[str]:
    names: set[str] = set()
    sources = [
        ROOT / "AGENTS.md",
        ROOT / "MyRole.txt",
        ROOT / "README.md",
        ROOT / "QUICK-START.md",
    ]
    sources.extend((ROOT / ".cursor" / "workflows").glob("*.md"))
    sources.extend((ROOT / ".cursor" / "skills").glob("*/SKILL.md"))
    known_disk = _skills_on_disk()
    # Canonical list line in AGENTS / MyRole often names skills with backticks
    for path in sources:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for match in SKILL_NAME.finditer(text):
            name = match.group(1)
            if name in known_disk or name in {
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
                names.add(name)
    # Explicit canonical line
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8") if (ROOT / "AGENTS.md").is_file() else ""
    for line in agents.splitlines():
        if "Canonical expert skills:" in line or line.strip().startswith("Canonical expert skills"):
            for match in SKILL_NAME.finditer(line):
                names.add(match.group(1))
    return names


def _path_exists(raw: str) -> bool:
    cleaned = raw.strip().strip("`")
    if cleaned in ALLOW_RUNTIME:
        return True
    if "*" in cleaned or "YYYY" in cleaned or "WID-XXXX" in cleaned:
        return True
    if any(tok in cleaned for tok in ("<", "…", "...")):
        # placeholder path — check template counterpart when obvious
        probe = PLACEHOLDER.sub("_TEMPLATE", cleaned)
        probe = probe.replace("<id>", "_TEMPLATE").replace("<WID>", "_TEMPLATE")
        path = ROOT / probe
        if path.exists():
            return True
        # journals/work-items/<id>/... → journals/work-items/_TEMPLATE/...
        alt = re.sub(r"work-items/[^/]+/", "work-items/_TEMPLATE/", cleaned)
        if (ROOT / alt).exists():
            return True
        return True  # runtime path with placeholder
    path = ROOT / cleaned
    return path.exists()


def main() -> int:
    findings: list[str] = []
    on_disk = _skills_on_disk()
    for name in sorted(_named_skills()):
        if name not in on_disk:
            findings.append(f"missing skill folder: .cursor/skills/{name}/")

    docs = []
    for pattern in ("**/*.md", "**/*.txt", "**/*.py"):
        docs.extend(ROOT.glob(pattern))
    for path in docs:
        if any(part in {".git", "__pycache__", "node_modules"} for part in path.parts):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            continue
        rel = path.relative_to(ROOT).as_posix()
        if path.suffix == ".md":
            for line in text.splitlines():
                if line.startswith("\\#"):
                    findings.append(f"escaped heading in {rel}: {line[:60]}")
        for match in BACKTICK_PATH.finditer(text):
            raw = match.group(1)
            if raw.endswith("/") or raw.endswith("\\"):
                continue
            if not _path_exists(raw):
                # skip obviously descriptive fragments
                if " " in raw or raw.count("/") == 0 and raw not in {
                    "AGENTS.md",
                    "MyRole.txt",
                    "README.md",
                    "QUICK-START.md",
                    "DESIGN.md",
                }:
                    continue
                findings.append(f"missing path in {rel}: `{raw}`")

        if "TRIGGER-INDEX" in rel or "trigger-index" in rel:
            continue
        if path.suffix in {".md", ".txt"}:
            if re.search(r"(?i)[a-z]wid-", text):
                findings.append(f"stale *wid- token in {rel}")
            if "2027-" in text:
                findings.append(f"2027- leftover in {rel}")

    registry = ROOT / ".cursor" / "workflows" / "workflow-registry.json"
    if registry.is_file():
        try:
            data = json.loads(registry.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            findings.append("workflow-registry.json is not valid JSON")
            data = {}
        workflows = data.get("workflows") if isinstance(data, dict) else None
        if isinstance(workflows, list):
            for entry in workflows:
                if not isinstance(entry, dict):
                    continue
                instr = entry.get("instruction_file") or entry.get("file")
                if isinstance(instr, str) and instr.strip():
                    if not (ROOT / instr).is_file() and not (
                        ROOT / ".cursor" / "workflows" / Path(instr).name
                    ).is_file():
                        findings.append(f"missing instruction_file: {instr}")
        elif isinstance(workflows, dict):
            for _key, entry in workflows.items():
                if not isinstance(entry, dict):
                    continue
                instr = entry.get("instruction_file") or entry.get("file")
                if isinstance(instr, str) and instr.strip():
                    candidate = ROOT / instr
                    alt = ROOT / ".cursor" / "workflows" / Path(instr).name
                    if not candidate.is_file() and not alt.is_file():
                        findings.append(f"missing instruction_file: {instr}")

    known = _load_known_tokens()
    if known:
        trigger_re = re.compile(r"\b(write:[a-z0-9_-]+|git:[a-z0-9_-]+|pr:[a-z0-9_-]+|sql:[a-z0-9_-]+|config:[a-z0-9_-]+)\b")
        for path in list((ROOT / ".cursor" / "skills").glob("*/SKILL.md")) + [
            ROOT / "facts" / "MEMORY-INDEX.md"
        ]:
            if not path.is_file():
                continue
            for match in trigger_re.finditer(path.read_text(encoding="utf-8")):
                tok = match.group(1)
                if tok not in known and tok != "none":
                    findings.append(
                        f"unknown trigger `{tok}` in {path.relative_to(ROOT).as_posix()}"
                    )

    readme = ROOT / "README.md"
    quick = ROOT / "QUICK-START.md"
    if readme.is_file() and quick.is_file():
        if readme.read_bytes() != quick.read_bytes():
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
