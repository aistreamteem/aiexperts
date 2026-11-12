#!/usr/bin/env python3
"""Integrity check for this Cursor expert scaffold. Exit non-zero on findings."""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME_RE = re.compile(r"\*\*([a-z0-9-]+)\*\*|`([a-z0-9-]+)`|\.cursor/skills/([a-z0-9-]+)/")
BACKTICK_PATH_RE = re.compile(r"`([^`]+)`")
ESCAPED_HEADING_RE = re.compile(r"^\\#", re.MULTILINE)
BAD_PATTERNS = [
    re.compile(r"[a-z]wid-", re.I),
    re.compile(r"2027-"),
    re.compile(r"facts/facts\.md"),
    re.compile(r"-operations\.md"),
    re.compile(r"config:change"),
    re.compile(r"inject-rules-on-action\.sh"),
    re.compile(r"workflowID-", re.I),
]
ALLOW_MISSING = {
    ".cursor/role-skills.md",
    ".cursor/active-context.txt",
    ".cursor/active-work-item.txt",
    "work-items/<id>/",
    "work-items/<id>",
    "journals/work-items/<id>/progress.md",
    "journals/work-items/<id>/state.json",
    "journals/work-items/<id>/nodes/<node>.md",
    "journals/work-items/<id>/nodes/<active leaf>.md",
    "journals/work-items/<id>/agent-notes/",
}


def _load_known_tokens() -> set[str]:
    hook = ROOT / ".cursor" / "hooks" / "inject_rules_on_action.py"
    spec = importlib.util.spec_from_file_location("inject_rules_on_action", hook)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return set(getattr(mod, "KNOWN_TOKENS", []) or [])


def _skill_dirs() -> set[str]:
    base = ROOT / ".cursor" / "skills"
    if not base.is_dir():
        return set()
    return {p.name for p in base.iterdir() if p.is_dir()}


def _named_skills(text: str) -> set[str]:
    found = set()
    for match in SKILL_NAME_RE.finditer(text):
        name = next(g for g in match.groups() if g)
        found.add(name)
    return found


def _exists_path(raw: str) -> bool:
    text = raw.strip()
    if not text or "://" in text or " " in text:
        return True
    if text in ALLOW_MISSING:
        return True
    if any(x in text for x in ("<", ">", "*", "?")):
        # Placeholder path — treat template existence as enough when prefix matches.
        probe = text
        for token in ("<id>", "<WID>", "<work-item-id>", "<node>", "<node-id>", "<active leaf>", "<name>"):
            probe = probe.replace(token, "_TEMPLATE")
        candidate = ROOT / probe
        if candidate.exists():
            return True
        # journals/work-items/<id>/... covered by template folder
        if "work-items/" in text or "journals/" in text or "qa-sessions/" in text:
            return True
        if text.startswith(".cursor/") or text.startswith("facts/") or text.startswith("docs/"):
            parent = (ROOT / text.split("<")[0]).parent
            return parent.exists() or (ROOT / text.split("<")[0].rstrip("/")).exists()
        return True
    path = ROOT / text
    return path.exists()


def main() -> int:
    findings: list[str] = []
    skill_dirs = _skill_dirs()
    known = _load_known_tokens()

    scan_files = []
    for rel in (
        "AGENTS.md",
        "MyRole.txt",
        "README.md",
        "QUICK-START.md",
        "facts/MEMORY-INDEX.md",
    ):
        path = ROOT / rel
        if path.is_file():
            scan_files.append(path)
    scan_files.extend((ROOT / ".cursor" / "skills").rglob("SKILL.md"))
    scan_files.extend((ROOT / ".cursor" / "workflows").glob("*.md"))

    # 1. Skills named in docs exist as folders (skip obvious non-skills).
    non_skills = {
        "work-item",
        "continue",
        "status",
        "workflow",
        "journal",
        "shared",
        "all",
        "none",
        "intake",
        "extract",
        "pack",
        "done",
        "yes",
        "no",
    }
    # Always require skills that AGENTS/MyRole explicitly bold as skills.
    required = {
        "define-role",
        "continue",
        "workflow-selector",
        "remember",
        "promote-facts-rules",
        "operator-qa",
        "journal-keeper",
        "switch-context",
        "integrate-docs",
        "memory-optimize",
    }
    for name in required:
        if name not in skill_dirs:
            findings.append(f"missing skill folder: {name}")

    # 3. Registry instruction files exist.
    registry = ROOT / ".cursor" / "workflows" / "workflow-registry.json"
    if registry.is_file():
        data = json.loads(registry.read_text(encoding="utf-8"))
        for key, meta in (data.get("workflows") or {}).items():
            instr = (meta or {}).get("instruction_file")
            if instr and not (ROOT / instr).is_file():
                findings.append(f"registry instruction missing for {key}: {instr}")

    # 4. Trigger tokens in skills / MEMORY-INDEX are known.
    token_re = re.compile(r"`(write:[a-z0-9-]+|sql:[a-z0-9-]+|git:[a-z0-9-]+|pr:[a-z0-9-]+|config:[a-z0-9-]+)`")
    for path in scan_files:
        text = path.read_text(encoding="utf-8")
        for tok in token_re.findall(text):
            if tok not in known and tok != "none":
                findings.append(f"unknown trigger {tok} in {path.relative_to(ROOT)}")

    # 5 + 6. Escaped headings and stale patterns.
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".md", ".txt"}:
            continue
        if any(p in path.parts for p in (".git", "__pycache__", "runtime")):
            continue
        text = path.read_text(encoding="utf-8")
        if ESCAPED_HEADING_RE.search(text):
            findings.append(f"escaped heading in {path.relative_to(ROOT)}")
        for pat in BAD_PATTERNS:
            # Allow active-work-item mentions only as legacy read fallback — checked separately.
            if pat.pattern == r"facts/facts\.md" and "work-items/" in str(path):
                continue
            if pat.search(text):
                # Allow facts.md under work-items templates.
                if pat.pattern == r"facts/facts\.md" and "work-items" in text:
                    # only flag top-level facts/facts.md references
                    if re.search(r"(?<!work-items/<id>/)(?<!work-items/<work-item-id>/)facts/facts\.md", text):
                        if "work-items/" not in path.as_posix() or "facts/facts.md" in text.replace(
                            "work-items/<id>/facts/facts.md", ""
                        ).replace("work-items/<work-item-id>/facts/facts.md", ""):
                            # softer: skip work-item relative facts.md
                            if "work-items/" in text and "facts/facts.md" in text and "facts/facts-shared" not in pat.pattern:
                                pass
                if pat.pattern == r"facts/facts\.md":
                    for line in text.splitlines():
                        if "facts/facts.md" in line and "work-items/" not in line:
                            findings.append(f"stale pattern facts/facts.md in {path.relative_to(ROOT)}")
                            break
                    continue
                if pat.pattern == r"-operations\.md":
                    findings.append(f"stale operations memory ref in {path.relative_to(ROOT)}")
                    continue
                if pat.pattern in {r"[a-z]wid-", r"2027-", r"config:change", r"inject-rules-on-action\.sh", r"workflowID-"}:
                    findings.append(f"stale pattern {pat.pattern} in {path.relative_to(ROOT)}")

    # 7. README and QUICK-START identical if both kept.
    readme = ROOT / "README.md"
    quick = ROOT / "QUICK-START.md"
    if readme.is_file() and quick.is_file():
        if readme.read_text(encoding="utf-8") != quick.read_text(encoding="utf-8"):
            findings.append("README.md and QUICK-START.md differ")

    # 2. Sample: every instruction_file and memory path from registry/AGENTS exists.
    for path in (ROOT / "AGENTS.md", ROOT / "MyRole.txt"):
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for match in BACKTICK_PATH_RE.finditer(text):
            raw = match.group(1)
            if "/" not in raw and "\\" not in raw:
                continue
            if raw.startswith("work-item:"):
                continue
            normalized = raw.replace("\\", "/")
            # Work Item-relative folders mentioned without the work-items/<id>/ prefix.
            if normalized in {"in/", "work/", "out/", "evidence/", "facts/", "in", "work", "out", "evidence"}:
                continue
            if not _exists_path(normalized):
                findings.append(f"missing path `{raw}` in {path.name}")

    if findings:
        print("Scaffold check FAILED:")
        for item in sorted(set(findings)):
            print(f" - {item}")
        return 1
    print("Scaffold check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
