#!/usr/bin/env python3
"""Integrity checks for this Claude expert scaffold. Exit non-zero on findings."""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALLOW_MISSING = {
    ".claude/role-skills.md",
    ".claude/active-work-item.txt",  # legacy; may be absent
    ".claude/plans/",
}

SKILL_NAME_RE = re.compile(
    r"\b(hld-writer|dd-writer|task-breakdown|git-workflow|implement-feature|"
    r"iterative-feature|scaffold-project|diagram-generator|spec-parser|"
    r"journal-keeper|continue|workflow-selector|switch-context|remember|"
    r"promote-facts-rules|integrate-docs|memory-optimize|define-role|"
    r"operator-qa|refactor|visual-page)\b"
)
BACKTICK_PATH_RE = re.compile(r"`([^`]+)`")
ESCAPED_HEADING_RE = re.compile(r"^\\#", re.MULTILINE)
BAD_PATTERNS = [
    (re.compile(r"(?i)[a-z]wid-"), "corrupted '…wid-' / workflowID- style text"),
    (re.compile(r"2027-"), "future seed date 2027-"),
    (re.compile(r"(?<!work-items/<id>/)facts/facts\.md"), "legacy facts/facts.md"),
    (re.compile(r"-operations\.md"), None),  # allowed for this role; skip
]


def _load_known_tokens() -> set[str]:
    hook = ROOT / ".claude" / "hooks" / "inject_rules_on_action.py"
    spec = importlib.util.spec_from_file_location("inject_rules_on_action", hook)
    if spec is None or spec.loader is None:
        return set()
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return set(getattr(mod, "KNOWN_TOKENS", []))


def _skills_on_disk() -> set[str]:
    base = ROOT / ".claude" / "skills"
    if not base.is_dir():
        return set()
    return {p.name for p in base.iterdir() if p.is_dir()}


def check_named_skills(findings: list[str]) -> None:
    on_disk = _skills_on_disk()
    texts: list[Path] = [
        ROOT / "CLAUDE.md",
        ROOT / "MyRole.txt",
        ROOT / "README.md",
        ROOT / "QUICK-START.md",
    ]
    texts += list((ROOT / ".claude" / "skills").rglob("SKILL.md"))
    texts += list((ROOT / ".claude" / "workflows").glob("*.md"))
    mentioned: set[str] = set()
    for path in texts:
        if not path.is_file():
            continue
        for match in SKILL_NAME_RE.finditer(path.read_text(encoding="utf-8", errors="replace")):
            mentioned.add(match.group(1))
    # Role does not require developer phase skills even if leftover folders mention them
    role_required = {
        "journal-keeper",
        "continue",
        "workflow-selector",
        "switch-context",
        "remember",
        "promote-facts-rules",
        "integrate-docs",
        "memory-optimize",
        "define-role",
        "operator-qa",
    }
    for name in sorted(role_required):
        if name not in on_disk:
            findings.append(f"missing required skill folder: .claude/skills/{name}/")
    for name in sorted(mentioned & role_required):
        if name not in on_disk:
            findings.append(f"named skill has no folder: {name}")


def check_registry(findings: list[str]) -> None:
    reg = ROOT / ".claude" / "workflows" / "workflow-registry.json"
    if not reg.is_file():
        findings.append("missing workflow-registry.json")
        return
    try:
        data = json.loads(reg.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        findings.append(f"workflow-registry.json invalid: {exc}")
        return
    workflows = data.get("workflows") if isinstance(data, dict) else None
    if not isinstance(workflows, list):
        # tolerate alternate shapes
        if isinstance(data, list):
            workflows = data
        elif isinstance(data, dict):
            workflows = list(data.values())
        else:
            findings.append("workflow-registry.json: unexpected shape")
            return
    for entry in workflows:
        if not isinstance(entry, dict):
            continue
        instr = entry.get("instruction_file") or entry.get("file") or entry.get("path")
        if not instr:
            continue
        path = ROOT / str(instr).replace("\\", "/")
        if not path.is_file():
            # also try under .claude/workflows/
            alt = ROOT / ".claude" / "workflows" / Path(str(instr)).name
            if not alt.is_file():
                findings.append(f"registry instruction_file missing: {instr}")


def check_triggers(findings: list[str]) -> None:
    known = _load_known_tokens()
    if not known:
        findings.append("KNOWN_TOKENS empty or hook missing")
        return
    token_re = re.compile(r"\*\*Triggers:\*\*\s*(.+)$")
    vocab_re = re.compile(r"`(write:[a-z]+|sql:[a-z]+|git:[a-z]+|pr:[a-z]+|config:[a-z]+)`")
    for path in list((ROOT / "facts").glob("*.md")) + list(
        (ROOT / ".claude" / "skills").rglob("SKILL.md")
    ):
        text = path.read_text(encoding="utf-8", errors="replace")
        for line in text.splitlines():
            m = token_re.match(line.strip())
            if m:
                for tok in re.split(r"[,\s]+", m.group(1).strip()):
                    if tok and tok != "none" and tok not in known:
                        findings.append(
                            f"{path.relative_to(ROOT)}: trigger `{tok}` not in KNOWN_TOKENS"
                        )
            for tok in vocab_re.findall(line):
                if tok not in known and tok != "none":
                    # vocabulary mention outside Triggers line
                    if "Triggers" in line or "trigger" in line.lower() or "write:doc" in line:
                        if tok not in known:
                            findings.append(
                                f"{path.relative_to(ROOT)}: vocabulary `{tok}` not in KNOWN_TOKENS"
                            )


def check_escaped(findings: list[str]) -> None:
    for path in ROOT.rglob("*.md"):
        if "node_modules" in path.parts:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if ESCAPED_HEADING_RE.search(text):
            findings.append(f"escaped heading in {path.relative_to(ROOT)}")


def check_bad_patterns(findings: list[str]) -> None:
    self_path = Path(__file__).resolve()
    for path in ROOT.rglob("*"):
        if path.suffix.lower() not in {".md", ".py", ".txt", ".json"}:
            continue
        if path.resolve() == self_path:
            continue
        if path.name in {"TRIGGER-INDEX.md", "trigger-index.json", "check_scaffold.py"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if re.search(r"(?i)workflowID-|folloWID-|newID-workflow", text):
            findings.append(f"corrupted ID insertion in {path.relative_to(ROOT)}")
        if "2027-" in text:
            findings.append(f"future date 2027- in {path.relative_to(ROOT)}")
        # Fat shell merge/audit scripts were replaced by Python. Thin .sh wrappers
        # under .claude/hooks/ that exec the Python entry points are allowed for Claude.
        if "merge-agent-notes.sh" in text or "post-journal-update.sh" in text:
            findings.append(f"stale fat shell hook in {path.relative_to(ROOT)}")
        rel = path.relative_to(ROOT).as_posix()
        if "inject-rules-on-action.sh" in text and not (
            rel.startswith(".claude/hooks/") or rel == ".claude/settings.json"
        ):
            # Docs/skills should name the Python classifier, not the thin wrapper.
            findings.append(f"stale shell classifier name in {rel}")


def check_readme_pair(findings: list[str]) -> None:
    readme = ROOT / "README.md"
    quick = ROOT / "QUICK-START.md"
    if not (readme.is_file() and quick.is_file()):
        return
    a = readme.read_text(encoding="utf-8")
    b = quick.read_text(encoding="utf-8")
    if a == b:
        return
    # Allow one file to be a short pointer to the other
    pointer = re.compile(
        r"(?is)^\s*#?.*\n+See\s+`(README|QUICK-START)\.md`\.?\s*$"
    )
    if pointer.match(a.strip()) or pointer.match(b.strip()) or (
        len(a) < 120 and "QUICK-START.md" in a
    ) or (len(b) < 120 and "README.md" in b):
        return
    findings.append("README.md and QUICK-START.md differ (plan expects identity if both kept)")


def main() -> int:
    findings: list[str] = []
    check_named_skills(findings)
    check_registry(findings)
    check_triggers(findings)
    check_escaped(findings)
    check_bad_patterns(findings)
    check_readme_pair(findings)

    if findings:
        print("scaffold check FAILED:")
        for item in findings:
            print(f"  - {item}")
        return 1
    print("scaffold check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
