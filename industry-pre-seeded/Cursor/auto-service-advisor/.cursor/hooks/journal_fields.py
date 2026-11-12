"""Shared journal field reader and active-work-item lookup for hooks."""

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


def active_work_id(root: Path) -> str:
    """Work item id from active-context.txt, with legacy pointer fallback."""
    context = root / ".cursor" / "active-context.txt"
    if context.is_file():
        lines = [ln.strip() for ln in read_text(context).splitlines() if ln.strip()]
        if lines:
            line = lines[0]
            if line.startswith("work-item:"):
                return line.split(":", 1)[1].strip()
            return line
    pointer = root / ".cursor" / "active-work-item.txt"
    if pointer.is_file():
        lines = [ln.strip() for ln in read_text(pointer).splitlines() if ln.strip()]
        if lines:
            return lines[0]
    expert = root / "journals" / "expert" / "progress.md"
    if expert.is_file():
        return field(read_text(expert), "Current work item")
    return ""


def active_leaf(root: Path, work_id: str) -> tuple[str, Path | None]:
    """Return (leaf_id, node_path) from state.json active path."""
    state_path = root / "journals" / "work-items" / work_id / "state.json"
    if not state_path.is_file():
        return "", None
    import json

    try:
        state = json.loads(read_text(state_path))
    except json.JSONDecodeError:
        return "", None
    active = state.get("active") if isinstance(state, dict) else []
    if not isinstance(active, list) or not active:
        return "", None
    leaf = active[-1]
    if not isinstance(leaf, str) or not leaf.strip():
        return "", None
    leaf = leaf.strip()
    if "/" in leaf or "\\" in leaf or ".." in leaf:
        return "", None
    node = root / "journals" / "work-items" / work_id / "nodes" / f"{leaf}.md"
    return leaf, node if node.is_file() else None
