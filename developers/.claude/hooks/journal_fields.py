"""Shared helpers for the journal, merge, snapshot and stop hooks (stdlib only)."""

from __future__ import annotations

import json
import re
from pathlib import Path

_FIELD = re.compile(
    r"^\s*(?:[-*]\s+)?\*{0,2}(?P<name>[^:*]+?)\*{0,2}\s*:\s*\*{0,2}\s*(?P<value>.*?)\s*$"
)


def read(path: Path) -> str:
    """Read a text file; return "" when it is missing or unreadable."""
    try:
        return Path(path).read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return ""


def field(text: str, name: str) -> str:
    """Value of a `Name: value` line, with or without bold markers."""
    wanted = name.lower()
    for line in text.splitlines():
        match = _FIELD.match(line)
        if match and match.group("name").strip().lower() == wanted:
            return match.group("value")
    return ""


def _first_line(path: Path) -> str:
    for line in read(path).splitlines():
        if line.strip():
            return line.strip()
    return ""


def active_work_id(root: Path) -> str:
    """Active work item id: active-context.txt, legacy pointer, expert journal."""
    root = Path(root)
    line = _first_line(root / ".claude" / "active-context.txt")
    if line.startswith("work-item:"):
        value = line.split(":", 1)[1].strip()
        if value:
            return value
    legacy = _first_line(root / ".claude" / "active-work-item.txt")
    if legacy:
        return legacy
    return field(read(root / "journals" / "expert" / "progress.md"), "Current work item")


def load_state(root: Path, work_id: str) -> dict:
    """Parsed state.json for a work item ({} when missing or invalid)."""
    path = Path(root) / "journals" / "work-items" / work_id / "state.json"
    try:
        state = json.loads(read(path)) if path.is_file() else {}
    except json.JSONDecodeError:
        return {}
    return state if isinstance(state, dict) else {}


def active_path(root: Path, work_id: str) -> list[str]:
    """The `active` branch path from state.json, with unsafe ids removed."""
    active = load_state(root, work_id).get("active")
    if not isinstance(active, list):
        return []
    return [
        node.strip()
        for node in active
        if isinstance(node, str)
        and node.strip()
        and "/" not in node
        and "\\" not in node
        and ".." not in node
    ]


def active_leaf(root: Path, work_id: str) -> str:
    """Last node of the active path in state.json ("" when none)."""
    path = active_path(root, work_id)
    return path[-1] if path else ""
