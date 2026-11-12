"""Shared journal field parsing and active-work-item lookup for hooks."""

from __future__ import annotations

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


def current_work_item(text: str) -> str:
    return field(text, "Current work item")


def work_id(root: Path, expert_text: str = "") -> str:
    """Active work item from active-context, legacy pointer, or expert journal."""
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
    if not expert_text:
        expert_text = read_text(root / "journals" / "expert" / "progress.md")
    return current_work_item(expert_text)


def active_leaf(root: Path, work_item_id: str) -> str:
    state_path = root / "journals" / "work-items" / work_item_id / "state.json"
    if not state_path.is_file():
        return ""
    try:
        import json

        state = json.loads(read_text(state_path))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return ""
    active = state.get("active") if isinstance(state, dict) else None
    if not isinstance(active, list) or not active:
        return ""
    leaf = active[-1]
    if not isinstance(leaf, str):
        return ""
    leaf = leaf.strip()
    if not leaf or "/" in leaf or "\\" in leaf or ".." in leaf:
        return ""
    return leaf


def active_phase(root: Path, work_item_id: str) -> str:
    state_path = root / "journals" / "work-items" / work_item_id / "state.json"
    if not state_path.is_file():
        return ""
    try:
        import json

        state = json.loads(read_text(state_path))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return ""
    active = state.get("active") if isinstance(state, dict) else None
    if not isinstance(active, list) or not active:
        return ""
    # Prefer a phase-like node after work-item when present.
    for node in reversed(active):
        if isinstance(node, str) and node.strip() and node.strip() != "work-item":
            return node.strip()
    last = active[-1]
    return last.strip() if isinstance(last, str) else ""
