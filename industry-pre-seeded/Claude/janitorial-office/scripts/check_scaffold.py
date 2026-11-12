#!/usr/bin/env python3
"""Integrity checks for this role expert scaffold. Exit non-zero on findings."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ALLOW_MISSING = {
    ".claude/role-skills.md",
    ".claude/active-work-item.txt",  # legacy read fallback; may be absent
    ".claude/plans/",
}

SKILL_NAME_RE = re.compile(
    r"\b(define-role|continue|workflow-selector|journal-keeper|remember|"
    r"promote-facts-rules|operator-qa|switch-context|integrate-docs|"
    r"memory-optimize|visual-page|spec-parser|implement-feature|"
    r"iterative-feature|refactor|scaffold-project|diagram-generator|"
    r"hld-writer|dd-writer|task-breakdown|git-workflow)\b"
)

PATH_RE = re.compile(r"`([^`]+)`")
PLACEHOLDER_RE = re.compile(r"(?i)<[^>]+>|\bWID\b")
def load_known_tokens() -> set[str]:
    import importlib.util

    path = ROOT / ".claude" / "hooks" / "inject_rules_on_action.py"
    spec = importlib.util.spec_from_file_location("inject_rules_on_action", path)
    if spec is None or spec.loader is None:
        return set()
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return set(getattr(mod, "KNOWN_TOKENS", []) or [])


def skill_folders() -> set[str]:
    base = ROOT / ".claude" / "skills"
    if not base.is_dir():
        return set()
    return {p.name for p in base.iterdir() if p.is_dir()}


def resolve_path(raw: str) -> bool:
    text = raw.strip()
    if not text or " " in text and not text.startswith("work-items"):
        return True  # not a path-like token
    if text.startswith("http") or text.endswith(".py`"):
        return True
    if any(text.startswith(a) or text.rstrip("/") in a for a in ALLOW_MISSING):
        return True
    # Skip command snippets and pure names
    if text in {"py -3", "python", "bash", "none", "all"}:
        return True
    if "/" not in text and "\\" not in text:
        return True
    cleaned = PLACEHOLDER_RE.sub("*", text.replace("\\", "/"))
    # Template-aware existence: if contains *, check parent templates
    if "*" in cleaned:
        # Treat as OK when a matching template root exists
        if "journals/work-items/" in cleaned:
            return (ROOT / "journals" / "work-items" / "_TEMPLATE").is_dir()
        if "work-items/" in cleaned:
            return (ROOT / "work-items" / "_TEMPLATE").is_dir()
        if "qa-sessions/" in cleaned:
            return (ROOT / "qa-sessions" / "_TEMPLATE").is_dir()
        return True
    candidate = ROOT / cleaned
    return candidate.exists()


def main() -> int:
    findings: list[str] = []
    folders = skill_folders()

    # 1. Skills named in key docs exist as folders (skip known-absent developer phase skills)
    skip_skills = {
        "hld-writer",
        "dd-writer",
        "task-breakdown",
        "git-workflow",
    }
    docs = [
        ROOT / "CLAUDE.md",
        ROOT / "MyRole.txt",
        ROOT / "README.md",
        ROOT / "QUICK-START.md",
    ]
    docs.extend((ROOT / ".claude" / "skills").rglob("SKILL.md"))
    docs.extend((ROOT / ".claude" / "workflows").glob("*.md"))
    named: set[str] = set()
    for doc in docs:
        if not doc.is_file():
            continue
        text = doc.read_text(encoding="utf-8", errors="replace")
        for match in SKILL_NAME_RE.finditer(text):
            named.add(match.group(1))
    for name in sorted(named):
        if name in skip_skills:
            continue
        if name not in folders:
            findings.append(f"missing skill folder: {name}")

    # 2. Registry instruction files exist
    registry = ROOT / ".claude" / "workflows" / "workflow-registry.json"
    if registry.is_file():
        data = json.loads(registry.read_text(encoding="utf-8"))
        workflows = data.get("workflows") if isinstance(data, dict) else None
        if isinstance(workflows, list):
            for entry in workflows:
                if not isinstance(entry, dict):
                    continue
                instr = entry.get("instruction_file") or entry.get("file")
                if isinstance(instr, str) and instr.strip():
                    path = ROOT / instr.replace("\\", "/")
                    if not path.is_file():
                        findings.append(f"registry missing instruction_file: {instr}")

    # 3. Trigger tokens in skills / MEMORY-INDEX are known
    known = load_known_tokens()
    known.add("none")
    trigger_re = re.compile(
        r"\b(write:file|write:sheet|write:doc|write:csv|write:sql|sql:generate|"
        r"pr:open|git:push|git:commit|config:change)\b"
    )
    for path in [ROOT / "facts" / "MEMORY-INDEX.md", *((ROOT / ".claude" / "skills").rglob("SKILL.md"))]:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for tok in trigger_re.findall(text):
            if tok not in known:
                findings.append(f"unknown trigger `{tok}` in {path.relative_to(ROOT)}")

    # 4. Escaped headings and leftover patterns
    for path in ROOT.rglob("*.md"):
        if any(part.startswith(".") and part not in {".claude"} for part in path.parts):
            continue
        if "node_modules" in path.parts:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if re.search(r"(?m)^\\#", text):
            findings.append(f"escaped heading in {path.relative_to(ROOT)}")
        if re.search(r"(?i)[a-z]wid-", text):
            findings.append(f"workflowID-corruption in {path.relative_to(ROOT)}")
        if "2027-" in text:
            findings.append(f"future archive date 2027- in {path.relative_to(ROOT)}")

    # 5. README / QUICK-START: identical or one clearly points at the other
    readme = ROOT / "README.md"
    quick = ROOT / "QUICK-START.md"
    if readme.is_file() and quick.is_file():
        a = readme.read_text(encoding="utf-8")
        b = quick.read_text(encoding="utf-8")
        if a != b:
            points = ("QUICK-START.md" in a) or ("README.md" in b)
            if not points:
                findings.append("README.md and QUICK-START.md differ without a pointer")

    # 6. No work-items/*/journal/ template
    if (ROOT / "work-items" / "_TEMPLATE" / "journal").exists():
        findings.append("work-items/_TEMPLATE/journal still present (D7)")

    if findings:
        print("Scaffold check FAILED:")
        for item in findings:
            print(f"  - {item}")
        return 1
    print("Scaffold check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
