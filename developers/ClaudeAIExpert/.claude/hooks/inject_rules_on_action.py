"""PreToolUse hook: inject expert rules that match the pending action.

Claude Code contract: read hook JSON on stdin, write
{"hookSpecificOutput": {"hookEventName": "PreToolUse", "additionalContext": "..."}}
and always exit 0.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

WRITE_TOOLS = {"Write", "Edit", "MultiEdit"}
SHELL_TOOLS = {"Bash", "Shell"}

HTML = (".html", ".htm")
DOC = (".md", ".markdown") + HTML


# One table per tool kind. This is the whole trigger vocabulary: a token that
# is not listed here can never be surfaced, and build_trigger_index.py warns
# about any rule tagged with one.
WRITE_TRIGGERS = [
    ("write:sql", lambda path: path.endswith(".sql")),
    ("sql:generate", lambda path: path.endswith(".sql")),
    ("write:doc", lambda path: path.endswith(DOC)),
]
SHELL_TRIGGERS = [
    ("pr:open", re.compile(r"\bgh\s+pr\s+create\b")),
    ("git:push", re.compile(r"\bgit\b[^;&|\n]*\bpush\b")),
    ("git:commit", re.compile(r"\bgit\b[^;&|\n]*\bcommit\b")),
]
KNOWN_TOKENS = [token for token, _ in WRITE_TRIGGERS + SHELL_TRIGGERS]


def _add(tokens: list[str], seen: set[str], *names: str) -> None:
    for name in names:
        if name not in seen:
            seen.add(name)
            tokens.append(name)


def classify(tool_name: str, file_path: str, command: str) -> list[str]:
    tokens: list[str] = []
    seen: set[str] = set()
    if tool_name in WRITE_TOOLS:
        path = file_path.replace("\\", "/").lower()
        for token, matches in WRITE_TRIGGERS:
            if matches(path):
                _add(tokens, seen, token)
    elif tool_name in SHELL_TOOLS:
        for token, pattern in SHELL_TRIGGERS:
            if pattern.search(command):
                _add(tokens, seen, token)
    return tokens


def _load_index(root: Path) -> dict:
    path = root / "facts" / "trigger-index.json"
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def additional_context(root: Path, payload: dict) -> str:
    tool_input = payload.get("tool_input") if isinstance(payload.get("tool_input"), dict) else {}
    tool_name = str(payload.get("tool_name") or "")
    file_path = str(tool_input.get("file_path") or tool_input.get("path") or "")
    command = str(tool_input.get("command") or "")
    tokens = classify(tool_name, file_path, command)
    if not tokens:
        return ""
    index = _load_index(root)
    rules: list[dict] = []
    seen: set[tuple[str, int]] = set()
    for token in tokens:
        entries = index.get(token) or []
        if not isinstance(entries, list):
            continue
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            key = (str(entry.get("file") or ""), int(entry.get("line") or 0))
            if key in seen:
                continue
            seen.add(key)
            body = str(entry.get("body") or "").strip()
            if body:
                rules.append(entry)
    if not rules:
        return ""
    matched = ", ".join(tokens)
    parts = [
        "⚠️ Expert rules for the action you are about to take "
        f"(matched triggers: {matched}). "
        "These apply REGARDLESS of the current workflow – follow them:",
        "",
    ]
    for entry in rules:
        parts.append("---")
        parts.append(str(entry.get("body") or "").rstrip())
        parts.append("")
    return "\n".join(parts).rstrip() + "\n"


def main() -> int:
    raw = sys.stdin.read()
    try:
        payload = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        payload = {}
    if not isinstance(payload, dict):
        payload = {}
    text = additional_context(Path.cwd(), payload)
    if text:
        json.dump(
            {"hookSpecificOutput": {"hookEventName": "PreToolUse", "additionalContext": text}},
            sys.stdout,
        )
        sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
