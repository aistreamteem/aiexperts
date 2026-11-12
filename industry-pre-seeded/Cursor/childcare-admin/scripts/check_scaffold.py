#!/usr/bin/env python3
"""Integrity check for the childcare-admin Cursor expert scaffold."""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALLOW_MISSING = {
    ".cursor/role-skills.md",
    ".cursor/active-context.txt",
    ".cursor/active-work-item.txt",
    ".cursor/active-qa-session.txt",
    ".cursor/plans/",
}
# Leftover developer skills may name paths this role does not ship.
SKIP_SKILL_FOLDERS = {
    "implement-feature",
    "iterative-feature",
    "refactor",
    "scaffold-project",
    "diagram-generator",
    "spec-parser",
}
CANONICAL_SKILLS = {
    "continue",
    "workflow-selector",
    "journal-keeper",
    "operator-qa",
    "remember",
    "integrate-docs",
    "promote-facts-rules",
    "switch-context",
    "memory-optimize",
    "define-role",
    "visual-page",
}
BACKTICK_PATH_RE = re.compile(r"`([^`]+)`")
NEGATION_RE = re.compile(
    r"(?i)(do not|don't|never|not invent|missing those|are not|instead of|rather than)"
)


def _fail(findings: list[str], msg: str) -> None:
    findings.append(msg)


def _load_known_tokens() -> set[str]:
    hook = ROOT / ".cursor" / "hooks" / "inject_rules_on_action.py"
    spec = importlib.util.spec_from_file_location("inject_rules_on_action", hook)
    if spec is None or spec.loader is None:
        return set()
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return set(getattr(mod, "KNOWN_TOKENS", []))


def _path_exists(raw: str) -> bool:
    path = raw.strip()
    if not path or path.startswith("http") or " " in path:
        return True
    if path in ALLOW_MISSING or any(path.startswith(a) for a in ALLOW_MISSING):
        return True
    if any(tok in path for tok in ("<", ">", "*", "?")):
        return True
    candidate = ROOT / path.replace("\\", "/")
    return candidate.exists()


def _scan_paths(doc: Path, text: str, findings: list[str]) -> None:
    for line in text.splitlines():
        if NEGATION_RE.search(line):
            continue
        for path in BACKTICK_PATH_RE.findall(line):
            if "/" not in path and "\\" not in path:
                continue
            if not path.startswith(
                (
                    "facts/",
                    "docs/",
                    "work-items/",
                    "journals/",
                    ".cursor/",
                    "scripts/",
                    "qa-sessions/",
                )
            ):
                continue
            if not _path_exists(path):
                _fail(
                    findings,
                    f"missing path `{path}` in {doc.relative_to(ROOT)}",
                )


def main() -> int:
    findings: list[str] = []
    skills_root = ROOT / ".cursor" / "skills"
    skills = {p.name for p in skills_root.iterdir() if p.is_dir()} if skills_root.is_dir() else set()

    for name in CANONICAL_SKILLS:
        if name not in skills:
            _fail(findings, f"missing skill folder .cursor/skills/{name}/")

    docs: list[Path] = [
        ROOT / "AGENTS.md",
        ROOT / "MyRole.txt",
        ROOT / "README.md",
        ROOT / ".cursor" / "CONTEXT-SYSTEM.md",
        ROOT / "facts" / "MEMORY-INDEX.md",
        ROOT / "facts" / "HOW-MEMORY-LOADING-WORKS.md",
    ]
    for name in CANONICAL_SKILLS:
        skill = skills_root / name / "SKILL.md"
        if skill.is_file():
            docs.append(skill)
    docs.extend((ROOT / ".cursor" / "workflows").glob("*.md"))

    known = _load_known_tokens()
    for doc in docs:
        if not doc.is_file():
            continue
        text = doc.read_text(encoding="utf-8")
        _scan_paths(doc, text, findings)
        if doc.name in {"MEMORY-INDEX.md"} or doc.parent.name in CANONICAL_SKILLS:
            for match in re.finditer(
                r"\*\*Triggers:\*\*\s*((?:`?[a-z]+:[a-z]+`?|none)(?:\s*[|,]\s*(?:`?[a-z]+:[a-z]+`?|none|\.\.\.))*)",
                text,
            ):
                for tok in re.split(r"[\s|,]+", match.group(1)):
                    tok = tok.strip().strip("`")
                    if not tok or tok in {"none", "..."}:
                        continue
                    if known and tok not in known:
                        _fail(
                            findings,
                            f"unknown trigger `{tok}` in {doc.relative_to(ROOT)}",
                        )
        for i, line in enumerate(text.splitlines(), 1):
            if re.search(r"(?i)[a-z]wid-", line) and "active-work-item" not in line:
                _fail(
                    findings,
                    f"stale ID splice in {doc.relative_to(ROOT)}:{i}: {line.strip()[:80]}",
                )
            if "2027-" in line:
                _fail(findings, f"future archive date in {doc.relative_to(ROOT)}:{i}")
            if line.lstrip().startswith("\\#"):
                _fail(findings, f"escaped heading in {doc.relative_to(ROOT)}:{i}")

    registry_path = ROOT / ".cursor" / "workflows" / "workflow-registry.json"
    if registry_path.is_file():
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
        for key, meta in (registry.get("workflows") or {}).items():
            instr = meta.get("instruction_file")
            if instr and not (ROOT / instr).is_file():
                _fail(findings, f"registry workflow {key} missing {instr}")

    # Fix 13 item 7 adapted: files may match, or one may point at the other.
    readme = ROOT / "README.md"
    quick = ROOT / "QUICK-START.md"
    if readme.is_file() and quick.is_file():
        r = readme.read_text(encoding="utf-8").strip()
        q = quick.read_text(encoding="utf-8").strip()
        if r != q and "QUICK-START.md" not in r and "README.md" not in q:
            _fail(
                findings,
                "README.md and QUICK-START.md differ (neither points at the other)",
            )

    if findings:
        print("check_scaffold FAILED:")
        for item in findings:
            print(f" - {item}")
        return 1
    print("check_scaffold OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
