#!/usr/bin/env python3
"""Integrity check for the expert scaffold (standard library only).

Almost every defect in the scaffold is a reference that went stale when
something was renamed or removed: a skill name, a path, a trigger token. This
script finds those, and exits non-zero on any finding.

Checks:
  1. Every skill named in CLAUDE.md, the skills, the workflow files, MyRole.txt
     and the README has a folder under .claude/skills/.
  2. Every backticked repository path in those files exists (placeholders such
     as <id> or <WID> act as wildcards). Paths created at run time are listed
     in RUNTIME_ALLOW below.
  3. Every instruction_file in workflow-registry.json exists.
  4. Every trigger token named in a skill or in MEMORY-INDEX.md is in the
     hook's KNOWN_TOKENS (or is `none`).
  5. No markdown file has a line that starts with an escaped hash (\\#).
  6. Stale text patterns from the repair are absent.
  7. README.md and QUICK-START.md are identical.

Run from anywhere:  python scripts/check_scaffold.py
"""

from __future__ import annotations

import fnmatch
import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / ".claude" / "skills"
HOOK_FILE = ROOT / ".claude" / "hooks" / "inject_rules_on_action.py"
REGISTRY = ROOT / ".claude" / "workflows" / "workflow-registry.json"

SKIP_DIRS = {".git", "__pycache__", "node_modules", ".venv", "venv"}

# Files that document the bugs and so quote the stale patterns on purpose.
STALE_SCAN_EXEMPT = {
    "EXPERT-REPAIR-PLAN.md",
    "VIRTUAL-EMPLOYEE-UPGRADE-IDEAS.md",
    "scripts/check_scaffold.py",
}

# --------------------------------------------------------------------------
# Check 1: skill names
# --------------------------------------------------------------------------

# Hyphenated phase names that are workflow phases of a pipeline that has no
# skill folder (the adhoc incident workflow), or plain jargon, not skills.
NON_SKILL_NAMES = {
    "assess-incident",
    "analyze-root-cause",
    "apply-mitigation",
    "monitor-impact",
    "resolve-and-document",
    "workflow-split",  # term for the split expert memory, not a skill
    "non-zero",  # exit-code jargon in workflow docs, not a skill
    # Developer-pipeline phase names this ops role does not invent (D1 N/A).
    "hld-writer",
    "dd-writer",
    "task-breakdown",
    "git-workflow",
    "test-writer",
    # Registered shipping / fulfillment jobs (workflow files, not skills).
    "bol-pack",
    "dim-vs-scale-exceptions",
    "end-of-day-manifest",
    "hold-and-will-call",
    "pack-exceptions",
    "pick-wave",
    "rma-returns",
    "short-ship-list",
    "tracking-exceptions",
}

# --------------------------------------------------------------------------
# Check 2: path allow-list (paths created at run time)
# --------------------------------------------------------------------------

# Exact repo-relative paths (forward slashes) that are written at run time or
# are legacy fallbacks that may legitimately be absent.
RUNTIME_ALLOW_EXACT = {
    ".claude/role-skills.md",
    ".claude/active-work-item.txt",  # legacy fallback, read only if present
    ".claude/active-context.txt",
    "docs/role/role-definition.md",
    "facts/TRIGGER-INDEX.md",
    "facts/trigger-index.json",
}

# Glob patterns (forward slashes, matched against the normalised reference,
# with each <placeholder> already replaced by *). Anything under these
# prefixes is produced by the pipeline while it runs.
RUNTIME_ALLOW_GLOBS = [
    "work-items/*",  # work-items/<id>/... exists as a template only
    "journals/work-items/*",  # journals/work-items/<id>/... likewise
    "qa-sessions/*",  # one folder per Q&A session
    "docs/design/*",  # HLD, DD, requirements summary
    "docs/diagrams/*",
    "docs/decisions/*",
    "docs/features/*",
    "docs/facts/*",
    "docs/incident/*",
    "docs/role/*",
    "tests/*",  # tests of the project being built, not of the scaffold
    "src/*",
    "outputs/*",
    ".claude/rules/*",
    "facts/rules-*.md",  # workflow-split memory files appear when captured
    "facts/facts-*.md",
    "facts/*ARCHIVE*",  # archives written by memory-optimize
    "facts/memory-analysis-*",
    ".claude/plans/*",  # optimisation plans written by memory-optimize
    ".claude/workflows/new-workflow.md",  # example name in workflows/README.md
    ".claude/active-qa-session.txt",  # pointer written by operator-qa
]

# Run-time names that are relative to a work item, a task folder, or the
# visual page, so they never exist at the repository root. Matched against the
# normalised reference (bare file names and relative folders).
RUNTIME_ALLOW_RELATIVE = [
    "dd.md", "hld.md", "spec.md", "manifest.json",
    "*ARCHIVE*",
    "tasks/*",
    "agent-notes/*",
    "whiteboard/*",
    # Work-item-relative folders used by this manufacturing-scheduler role.
    "in", "in/*", "work", "work/*", "out", "out/*",
    "evidence", "evidence/*", "rules", "rules/*", "facts", "facts/*",
    "_TEMPLATE", "_TEMPLATE/*", "_TEMPLATE/",
]

# Placeholder-built names such as facts/<topic>-<type>.md that only make sense
# once a user has chosen the topic. Applies only when the reference had a
# placeholder (so a typo like facts/facts-operations.md is still reported).
RUNTIME_ALLOW_PLACEHOLDER = [
    "facts/*-*.md",
]

# Placeholders: <id>, <WID>, <work-item-id>, <feature-id>, <node>,
# <active leaf>, <name> ... any angle-bracket group is a wildcard. A few other
# conventional forms are treated the same way.
PLACEHOLDER_RES = [
    re.compile(r"<[^<>`]+>"),
    re.compile(r"\bWID-(?:X+|N+|\d{1,2}|\.\.\.|…)"),
    re.compile(r"\bQ(?:NNN|\d+|\*)"),
    re.compile(r"\bYYYY(?:-MM(?:-DD)?)?"),
    re.compile(r"\[[^\[\]`]+\]"),
    re.compile(r"\{[^{}`]+\}"),
]

PATH_EXTS = (
    ".md", ".txt", ".json", ".py", ".sh", ".yml", ".yaml", ".html", ".js",
    ".mmd", ".sql", ".cmd", ".ps1", ".csv", ".toml",
)
TOP_DIRS = {
    ".claude", ".github", "docs", "facts", "journals", "qa-sessions",
    "scripts", "tests", "work-items", "src", "outputs",
}
PATH_CHARS = re.compile(r"^[\w.\-<>*{}\[\]/\\ …]+$")
BACKTICK_RE = re.compile(r"`([^`\n]+)`")

# --------------------------------------------------------------------------
# Check 4: trigger tokens
# --------------------------------------------------------------------------

TOKEN_RE = re.compile(r"^[a-z]+:[a-z][a-z-]*$")
# Prefixes that identify a trigger-looking token (rather than, say,
# `work-item:<id>`). The hook's own prefixes are added at run time.
EXTRA_TRIGGER_PREFIXES = {"read", "edit", "shell", "delete", "run", "tool", "file"}

# --------------------------------------------------------------------------
# Check 6: stale text patterns
# --------------------------------------------------------------------------

STALE_PATTERNS = [
    # Bad search-and-replace leftovers: workflow-, follow-up, new-workflow.
    # A letter must come immediately before "wid-", so WID-123 and
    # active-work-item are not matched.
    (re.compile(r"(?i)[a-z]wid-"), "search-and-replace leftover ([a-z]wid-)"),
    (re.compile(r"2027-"), "date typo (2027-)"),
    # This manufacturing-scheduler role keeps operations + shared pairs
    # (D4 adapted: do not invent developer/incident pairs).
]
FACTS_MD_RE = re.compile(r"(\S*)facts/facts\.md")

# --------------------------------------------------------------------------


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def walk_files() -> list[Path]:
    out: list[Path] = []
    for path in ROOT.rglob("*"):
        if any(part in SKIP_DIRS for part in path.relative_to(ROOT).parts):
            continue
        if path.is_file():
            out.append(path)
    return sorted(out)


def lineno(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


class Findings:
    def __init__(self) -> None:
        self.items: list[str] = []

    def add(self, check: int, where: str, message: str) -> None:
        self.items.append(f"[check {check}] {where}: {message}")


def doc_files(all_files: list[Path]) -> list[Path]:
    """Files whose skill names and paths are checked (checks 1 and 2)."""
    wanted: list[Path] = []
    for name in ("CLAUDE.md", "MyRole.txt", "README.md", "QUICK-START.md"):
        path = ROOT / name
        if path.is_file():
            wanted.append(path)
    wanted.extend(p for p in all_files if p.name == "SKILL.md" and SKILLS_DIR in p.parents)
    wanted.extend(
        p for p in all_files
        if (ROOT / ".claude" / "workflows") in p.parents and p.suffix == ".md"
    )
    context = ROOT / ".claude" / "CONTEXT-SYSTEM.md"
    if context.is_file():
        wanted.append(context)
    return wanted


# ---------------------------------------------------------------- check 1


def skill_references(text: str, skill_names: set[str]) -> list[tuple[int, str]]:
    """Return (position, name) for every place the text names a skill."""
    refs: list[tuple[int, str]] = []

    # **name** where the name is a known skill or is hyphenated lower-case.
    for m in re.finditer(r"\*\*([a-z][a-z0-9]*(?:-[a-z0-9]+)*)\*\*", text):
        name = m.group(1)
        if name in skill_names or "-" in name:
            refs.append((m.start(1), name))

    # the `name` skill / the name skill / skill `name`
    for m in re.finditer(r"`([a-z][a-z0-9]*(?:-[a-z0-9]+)*)`\s+skills?\b", text):
        refs.append((m.start(1), m.group(1)))
    for m in re.finditer(
        r"\b(?:run|use|call|calls|invoke|read|runs|using)\s+(?:the\s+)?"
        r"`?([a-z][a-z0-9]*(?:-[a-z0-9]+)+)`?(?:\s+skill\b)",
        text,
    ):
        refs.append((m.start(1), m.group(1)))
    for m in re.finditer(r"\bskills?\s+`([a-z][a-z0-9]*(?:-[a-z0-9]+)*)`", text):
        refs.append((m.start(1), m.group(1)))

    # Folder form: .claude/skills/<name>/
    for m in re.finditer(r"\.claude[/\\]skills[/\\]([a-z][a-z0-9-]*)[/\\]", text):
        refs.append((m.start(1), m.group(1)))

    # Pipeline phase chains:  a → b → c (loop)
    for m in re.finditer(r"^.*→.*$", text, flags=re.M):
        line = m.group(0)
        if "Phases:" not in line and not re.match(r"^\s*[a-z][a-z0-9-]*(\s+→\s+)", line):
            continue
        for tm in re.finditer(r"(?<![\w-])([a-z][a-z0-9]*(?:-[a-z0-9]+)+)(?![\w-])", line):
            refs.append((m.start() + tm.start(1), tm.group(1)))
    return refs


def check_skills(findings: Findings, docs: list[Path]) -> set[str]:
    skill_names = {p.name for p in SKILLS_DIR.iterdir() if p.is_dir()} if SKILLS_DIR.is_dir() else set()
    for doc in docs:
        text = read(doc)
        seen: set[str] = set()
        for pos, name in skill_references(text, skill_names):
            if name in skill_names or name in NON_SKILL_NAMES or name in seen:
                continue
            if (SKILLS_DIR / name / "SKILL.md").is_file():
                continue
            seen.add(name)
            findings.add(1, f"{rel(doc)}:{lineno(text, pos)}", f"skill '{name}' has no folder under .claude/skills/")
    for name in sorted(skill_names):
        if not (SKILLS_DIR / name / "SKILL.md").is_file():
            findings.add(1, f".claude/skills/{name}", "skill folder has no SKILL.md")
    return skill_names


# ---------------------------------------------------------------- check 2


def normalise_reference(token: str) -> str | None:
    """Turn a backticked token into a glob against repo-relative paths, or
    None when the token is not a repository path."""
    token = token.strip()
    if not token or token.startswith(("http://", "https://", "~", "$", "-", "#")):
        return None
    if re.match(r"^[A-Za-z]:[\\/]", token) or token.startswith(("/", "\\\\")):
        return None  # absolute paths are not repository paths
    if not PATH_CHARS.match(token):
        return None
    if " " in token:
        return None
    if token in {".", ".."} or token.startswith(("./", "../")):
        return None
    if token.startswith(".") and "/" not in token and token.count(".") == 1:
        return None  # a bare extension such as .sql
    path = token.replace("\\", "/")
    has_slash = "/" in path
    last = path.rstrip("/").rsplit("/", 1)[-1]
    looks_like_file = last.lower().endswith(PATH_EXTS) and not last.startswith(("*", "<"))
    first = path.split("/", 1)[0]
    if has_slash:
        if not (path.endswith("/") or looks_like_file or first in TOP_DIRS or first.startswith("<")):
            return None
    elif not looks_like_file:
        return None
    for placeholder in PLACEHOLDER_RES:
        path = placeholder.sub("*", path)
    path = path.replace("…", "*").replace("...", "*")
    return path.rstrip("/")


def reference_exists(pattern: str, doc: Path, all_paths: set[str], basenames: set[str]) -> bool:
    if pattern in all_paths:
        return True
    if any(ch in pattern for ch in "*?"):
        if any(fnmatch.fnmatchcase(p, pattern) for p in all_paths):
            return True
    if "/" not in pattern:
        # A bare file name: root, the doc's own folder, or any file by that name.
        if pattern in basenames:
            return True
        if any(ch in pattern for ch in "*?") and any(fnmatch.fnmatchcase(b, pattern) for b in basenames):
            return True
    else:
        # Relative to the referring file's folder (e.g. runtime/serve.py in a skill).
        local = (doc.parent / pattern).relative_to(ROOT).as_posix()
        if local in all_paths:
            return True
        if any(ch in pattern for ch in "*?") and any(fnmatch.fnmatchcase(p, local) for p in all_paths):
            return True
        # A work-item-relative path (nodes/work-item.md) that exists below some
        # template folder.
        if pattern.split("/", 1)[0] not in TOP_DIRS and any(
            fnmatch.fnmatchcase(p, "*/" + pattern) for p in all_paths
        ):
            return True
    return False


def is_runtime(pattern: str) -> bool:
    if pattern in RUNTIME_ALLOW_EXACT:
        return True
    # Test the folder itself as well as anything below it (docs/design and
    # docs/design/hld.md are both covered by "docs/design/*").
    candidates = (pattern, pattern + "/x")
    if any(fnmatch.fnmatchcase(c, g) for c in candidates for g in RUNTIME_ALLOW_GLOBS):
        return True
    if any(fnmatch.fnmatchcase(pattern, g) for g in RUNTIME_ALLOW_RELATIVE):
        return True
    if "*" in pattern and any(fnmatch.fnmatchcase(pattern, g) for g in RUNTIME_ALLOW_PLACEHOLDER):
        return True
    return False


def check_paths(findings: Findings, docs: list[Path], all_files: list[Path]) -> None:
    all_paths: set[str] = set()
    basenames: set[str] = set()
    for f in all_files:
        r = rel(f)
        all_paths.add(r)
        basenames.add(f.name)
        for parent in f.relative_to(ROOT).parents:
            if parent.as_posix() != ".":
                all_paths.add(parent.as_posix())
    for doc in docs:
        text = read(doc)
        in_fence = False
        offset = 0
        reported: set[str] = set()
        for line in text.splitlines(keepends=True):
            stripped = line.strip()
            if stripped.startswith("```"):
                in_fence = not in_fence
                offset += len(line)
                continue
            if not in_fence:
                for m in BACKTICK_RE.finditer(line):
                    pattern = normalise_reference(m.group(1))
                    if pattern is None or pattern in reported:
                        continue
                    if reference_exists(pattern, doc, all_paths, basenames) or is_runtime(pattern):
                        continue
                    reported.add(pattern)
                    findings.add(
                        2,
                        f"{rel(doc)}:{lineno(text, offset)}",
                        f"path `{m.group(1)}` does not exist (and is not an allow-listed runtime path)",
                    )
            offset += len(line)


# ---------------------------------------------------------------- check 3


def check_registry(findings: Findings) -> None:
    if not REGISTRY.is_file():
        findings.add(3, rel(REGISTRY), "workflow-registry.json is missing")
        return
    try:
        data = json.loads(read(REGISTRY))
    except json.JSONDecodeError as exc:
        findings.add(3, rel(REGISTRY), f"invalid JSON: {exc}")
        return
    workflows = data.get("workflows")
    if not isinstance(workflows, dict) or not workflows:
        findings.add(3, rel(REGISTRY), "no workflows listed")
        return
    for key, entry in workflows.items():
        instruction = entry.get("instruction_file") if isinstance(entry, dict) else None
        if not instruction:
            findings.add(3, rel(REGISTRY), f"workflow '{key}' has no instruction_file")
        elif not (ROOT / instruction).is_file():
            findings.add(3, rel(REGISTRY), f"workflow '{key}': instruction_file '{instruction}' does not exist")


# ---------------------------------------------------------------- check 4


def load_known_tokens() -> list[str]:
    spec = importlib.util.spec_from_file_location("inject_rules_on_action", HOOK_FILE)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {HOOK_FILE}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return list(module.KNOWN_TOKENS)


def trigger_tokens_in(text: str, prefixes: set[str]) -> list[tuple[int, str]]:
    found: list[tuple[int, str]] = []
    # Backticked tokens with a trigger-style prefix, e.g. `write:sql`.
    for m in BACKTICK_RE.finditer(text):
        token = m.group(1).strip()
        if TOKEN_RE.match(token) and token.split(":", 1)[0] in prefixes:
            found.append((m.start(1), token))
    # `**Triggers:** a | b, c` fields: the leading tokens of the value.
    for m in re.finditer(r"\*\*Triggers:\*\*[ \t]*([^\n]*)", text):
        value = m.group(1)
        for part in re.split(r"\s*[|,]\s*", value):
            first = part.strip().split(" ", 1)[0].strip("`")
            if re.match(r"^[a-z]+:[a-z][a-z-]*$", first) or first == "none":
                found.append((m.start(1), first))
            else:
                break  # prose after the vocabulary, or a placeholder like [..]
    return found


def check_triggers(findings: Findings, all_files: list[Path]) -> None:
    try:
        known = load_known_tokens()
    except Exception as exc:  # noqa: BLE001 - report any import failure
        findings.add(4, rel(HOOK_FILE), f"cannot import KNOWN_TOKENS: {exc}")
        return
    allowed = set(known) | {"none"}
    prefixes = {t.split(":", 1)[0] for t in known} | EXTRA_TRIGGER_PREFIXES
    sources = [p for p in all_files if p.name == "SKILL.md" and SKILLS_DIR in p.parents]
    index = ROOT / "facts" / "MEMORY-INDEX.md"
    if index.is_file():
        sources.append(index)
    for path in sources:
        text = read(path)
        for pos, token in trigger_tokens_in(text, prefixes):
            if token not in allowed:
                findings.add(4, f"{rel(path)}:{lineno(text, pos)}", f"trigger token '{token}' is not in KNOWN_TOKENS")


# ---------------------------------------------------------------- check 5


def check_escaped_hash(findings: Findings, all_files: list[Path]) -> None:
    for path in all_files:
        if path.suffix.lower() not in (".md", ".markdown"):
            continue
        for number, line in enumerate(read(path).splitlines(), start=1):
            if line.lstrip().startswith("\\#"):
                findings.add(5, f"{rel(path)}:{number}", "line starts with an escaped hash (\\#)")


# ---------------------------------------------------------------- check 6

TEXT_SUFFIXES = {".md", ".txt", ".json", ".py", ".sh", ".yml", ".yaml", ".html", ".js", ".mmd", ".toml", ".cmd", ".ps1", ".csv"}


def check_stale_text(findings: Findings, all_files: list[Path]) -> None:
    for path in all_files:
        r = rel(path)
        if r in STALE_SCAN_EXEMPT or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        text = read(path)
        for pattern, label in STALE_PATTERNS:
            for m in pattern.finditer(text):
                findings.add(6, f"{r}:{lineno(text, m.start())}", f"{label}: '{m.group(0)}'")
        for m in FACTS_MD_RE.finditer(text):
            if "work-items" in m.group(1) or r.startswith("work-items/"):
                continue  # work-items/<id>/facts/facts.md is legitimate
            findings.add(6, f"{r}:{lineno(text, m.start())}", "facts/facts.md outside work-items/ (expert memory is split by workflow)")


# ---------------------------------------------------------------- check 7


def check_readme_pair(findings: Findings) -> None:
    readme, quick = ROOT / "README.md", ROOT / "QUICK-START.md"
    if not readme.is_file() or not quick.is_file():
        return  # "identical, if both are kept"
    a = read(readme).replace("\r\n", "\n")
    b = read(quick).replace("\r\n", "\n")
    if a != b:
        findings.add(7, "README.md / QUICK-START.md", "files differ; keep them identical or remove one")


# --------------------------------------------------------------------------


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
        except (AttributeError, ValueError):
            pass
    findings = Findings()
    all_files = walk_files()
    docs = doc_files(all_files)
    check_skills(findings, docs)
    check_paths(findings, docs, all_files)
    check_registry(findings)
    check_triggers(findings, all_files)
    check_escaped_hash(findings, all_files)
    check_stale_text(findings, all_files)
    check_readme_pair(findings)
    if findings.items:
        for item in findings.items:
            print(item)
        print(f"\ncheck_scaffold: {len(findings.items)} finding(s)")
        return 1
    print(f"check_scaffold: OK ({len(docs)} documents, {len(all_files)} files scanned)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
