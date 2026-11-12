"""PreToolUse hook. Inject expert rules that match the action about to happen.

Program Manager triggers. Always exit 0.
Claude Code: {"hookSpecificOutput": {"hookEventName": "PreToolUse", "additionalContext": "..."}}
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

WRITE_TOOLS = {"Write", "Edit", "MultiEdit", "StrReplace", "EditNotebook"}

DOC = (".md", ".markdown", ".html", ".htm")

# One table for write tools. This is the whole trigger vocabulary: a token that
# is not listed here can never be surfaced, and build_trigger_index.py warns
# about any rule tagged with one.
WRITE_TRIGGERS = [
    ("raid:update", lambda path: "raid" in path),
    ("steering:pack", lambda path: "steering" in path),
    ("status:report", lambda path: "status" in path),
    ("milestone:review", lambda path: "milestone" in path),
    ("scope:change", lambda path: "changes/" in path or "scope" in path),
    ("write:doc", lambda path: path.endswith(DOC)),
]
KNOWN_TOKENS = [token for token, _ in WRITE_TRIGGERS]


def _add(tokens: list[str], seen: set[str], *names: str) -> None:
    for name in names:
        if name not in seen:
            seen.add(name)
            tokens.append(name)


def classify(tool_name: str, file_path: str, command: str = "") -> list[str]:
    del command  # reserved for future shell triggers; PM vocabulary is path-based
    tokens: list[str] = []
    seen: set[str] = set()
    if tool_name in WRITE_TOOLS:
        path = file_path.replace("\\", "/").lower()
        for token, matches in WRITE_TRIGGERS:
            if matches(path):
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
        "Follow them:\n\n"
        f"{bodies}"
    )


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
    tool_input = payload.get("tool_input") if isinstance(payload.get("tool_input"), dict) else {}
    tokens = classify(
        str(payload.get("tool_name") or ""),
        str(tool_input.get("file_path") or tool_input.get("path") or ""),
        str(tool_input.get("command") or ""),
    )
    text = context_text(tokens, matching_rules(index, tokens))
    if text:
        json.dump(
            {"hookSpecificOutput": {"hookEventName": "PreToolUse", "additionalContext": text}},
            sys.stdout,
        )
        sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
