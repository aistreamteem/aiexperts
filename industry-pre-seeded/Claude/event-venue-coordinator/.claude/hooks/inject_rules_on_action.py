"""PreToolUse hook. Inject expert rules that match the action about to run.

Reads facts/trigger-index.json. Claude Code contract: emit
{"hookSpecificOutput": {"hookEventName": "PreToolUse", "additionalContext": "..."}}
when a rule matches. Always exits 0.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

WRITE_TOOLS = {"Write", "StrReplace", "Edit", "MultiEdit", "EditNotebook"}
SHELL_TOOLS = {"Shell", "Bash"}

DOC = (".md", ".markdown", ".html", ".htm", ".txt")

# One table per tool kind. This is the whole trigger vocabulary for this role:
# pack/list markdown and CSV deliverables. A token not listed here can never
# be surfaced, and build_trigger_index.py warns about any rule tagged with one.
WRITE_TRIGGERS = [
    ("write:doc", lambda path: path.endswith(DOC)),
    ("write:csv", lambda path: path.endswith((".csv", ".tsv"))),
]
SHELL_TRIGGERS: list[tuple[str, re.Pattern[str]]] = [
    # Role packs are files, not git/PR flows. Shell only hints when a command
    # clearly names a pack/list deliverable extension.
    ("write:doc", re.compile(r"\.(?:md|markdown|html?|txt)\b", re.I)),
    ("write:csv", re.compile(r"\.(?:csv|tsv)\b", re.I)),
]
KNOWN_TOKENS = [token for token, _ in WRITE_TRIGGERS + SHELL_TRIGGERS]


def _tool_input(payload: dict) -> dict:
    raw = payload.get("tool_input")
    if isinstance(raw, dict):
        return raw
    if isinstance(raw, str) and raw.strip():
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            return {"command": raw}
        if isinstance(parsed, dict):
            return parsed
    return {}


def _file_path(payload: dict, tool_input: dict) -> str:
    for source in (tool_input, payload):
        for key in ("file_path", "path", "target_file"):
            value = source.get(key)
            if isinstance(value, str) and value.strip():
                return value.replace("\\", "/")
    return ""


def _add(tokens: list[str], seen: set[str], *names: str) -> None:
    for name in names:
        if name not in seen:
            seen.add(name)
            tokens.append(name)


def classify(tool_name: str, file_path: str, command: str) -> list[str]:
    tokens: list[str] = []
    seen: set[str] = set()
    if tool_name in WRITE_TOOLS:
        path = file_path.lower()
        for token, matches in WRITE_TRIGGERS:
            if matches(path):
                _add(tokens, seen, token)
    elif tool_name in SHELL_TOOLS:
        for token, pattern in SHELL_TRIGGERS:
            if pattern.search(command):
                _add(tokens, seen, token)
    return tokens


def matching_rules(index: dict, tokens: list[str]) -> list[dict]:
    found: list[dict] = []
    seen: set[str] = set()
    for token in tokens:
        entries = index.get(token)
        if not isinstance(entries, list):
            continue
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            key = f"{entry.get('file')}|{entry.get('line')}"
            if key in seen:
                continue
            body = entry.get("body")
            if not isinstance(body, str) or not body.strip():
                continue
            seen.add(key)
            found.append(entry)
    return found


def context_text(tokens: list[str], rules: list[dict]) -> str:
    if not rules:
        return ""
    bodies = "\n\n".join("---\n" + str(rule.get("body") or "") for rule in rules)
    joined = ", ".join(tokens)
    return (
        "Expert rules for the action you are about to take "
        f"(matched triggers: {joined}). "
        "These apply regardless of the current workflow:\n\n"
        f"{bodies}"
    )


def emit(text: str) -> None:
    if not text:
        return
    json.dump(
        {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "additionalContext": text,
            }
        },
        sys.stdout,
    )
    sys.stdout.write("\n")


def main() -> int:
    raw = sys.stdin.read()
    try:
        payload = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        payload = {}
    if not isinstance(payload, dict):
        payload = {}
    index_path = Path.cwd() / "facts" / "trigger-index.json"
    if not index_path.is_file():
        return 0
    try:
        index = json.loads(index_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return 0
    if not isinstance(index, dict):
        return 0
    tool_input = _tool_input(payload)
    tokens = classify(
        str(payload.get("tool_name") or ""),
        _file_path(payload, tool_input),
        str(tool_input.get("command") or ""),
    )
    emit(context_text(tokens, matching_rules(index, tokens)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
