"""Shared journal field reader and active-work-item lookup for hooks."""

from __future__ import annotations

import json
import re
from pathlib import Path

_FIELD = re.compile(
    r"^\s*(?:[-*]\s+)?\*{0,2}(?P<name>[^:*]+?)\*{0,2}\s*:\s*\*{0,2}\s*(?P<value>.*?)\s*$"
)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
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


def work_id(root: Path) -> str:
    context = root / ".cursor" / "active-context.txt"
    if context.is_file():
        lines = [ln.strip() for ln in read_text(context).splitlines() if ln.strip()]
        if lines and lines[0].startswith("work-item:"):
            return lines[0].split(":", 1)[1].strip()
    pointer = root / ".cursor" / "active-work-item.txt"
    if pointer.is_file():
        lines = [ln.strip() for ln in read_text(pointer).splitlines() if ln.strip()]
        if lines:
            return lines[0]
    expert = root / "journals" / "expert" / "progress.md"
    if expert.is_file():
        return field(read_text(expert), "Current work item")
    return ""


def active_leaf(root: Path, wid: str) -> str:
    state_path = root / "journals" / "work-items" / wid / "state.json"
    if not state_path.is_file():
        return ""
    try:
        state = json.loads(read_text(state_path) or "{}")
    except (OSError, UnicodeError, json.JSONDecodeError):
        return ""
    active = state.get("active") if isinstance(state, dict) else []
    if not isinstance(active, list) or not active:
        return ""
    leaf = active[-1]
    if not isinstance(leaf, str):
        return ""
    leaf = leaf.strip()
    if not leaf or "/" in leaf or "\\" in leaf or ".." in leaf:
        return ""
    return leaf


def active_phase(root: Path, wid: str) -> str:
    """Phase label from the active path (second node when present)."""
    state_path = root / "journals" / "work-items" / wid / "state.json"
    try:
        state = json.loads(read_text(state_path) or "{}")
    except (OSError, UnicodeError, json.JSONDecodeError):
        return ""
    active = state.get("active") if isinstance(state, dict) else []
    if not isinstance(active, list) or not active:
        return ""
    if len(active) >= 2 and isinstance(active[1], str):
        return active[1]
    if isinstance(active[0], str):
        return active[0]
    return ""
