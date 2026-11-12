"""Shared helpers for the journal hooks (active work item, active leaf, fields)."""

from __future__ import annotations

import json
import re
from pathlib import Path

_FIELD = re.compile(
    r"^\s*(?:[-*]\s+)?\*{0,2}(?P<name>[^:*]+?)\*{0,2}\s*:\s*\*{0,2}\s*(?P<value>.*?)\s*$"
)


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return ""


def _field(text: str, name: str) -> str:
    """Value of a `Name: value` line, with or without bold markers."""
    wanted = name.lower()
    for line in text.splitlines():
        match = _FIELD.match(line)
        if match and match.group("name").strip().lower() == wanted:
            return match.group("value")
    return ""


def _safe_id(value: str) -> str:
    value = value.strip()
    if not value or "/" in value or "\\" in value or ".." in value:
        return ""
    return value


def work_id(root: Path) -> str:
    """Active work item id: active-context, then active-work-item, then expert journal."""
    context = root / ".claude" / "active-context.txt"
    if context.is_file():
        lines = _read(context).splitlines()
        line = lines[0].strip() if lines else ""
        if line.startswith("work-item:"):
            found = _safe_id(line.split(":", 1)[1])
            if found:
                return found
    pointer = root / ".claude" / "active-work-item.txt"
    if pointer.is_file():
        lines = [line.strip() for line in _read(pointer).splitlines() if line.strip()]
        if lines and _safe_id(lines[0]):
            return lines[0]
    expert = root / "journals" / "expert" / "progress.md"
    return _safe_id(_field(_read(expert), "Current work item"))


def active_path(root: Path, wid: str) -> list[str]:
    """The `active` list from the work item's state.json (empty when unreadable)."""
    state_path = root / "journals" / "work-items" / wid / "state.json"
    try:
        state = json.loads(_read(state_path)) if state_path.is_file() else {}
    except json.JSONDecodeError:
        return []
    active = state.get("active") if isinstance(state, dict) else []
    if not isinstance(active, list):
        return []
    return [node.strip() for node in active if isinstance(node, str) and _safe_id(node)]


def active_leaf(root: Path, wid: str) -> str:
    path = active_path(root, wid)
    return path[-1] if path else ""


def node_path(root: Path, wid: str, leaf: str) -> Path:
    return root / "journals" / "work-items" / wid / "nodes" / f"{leaf}.md"
