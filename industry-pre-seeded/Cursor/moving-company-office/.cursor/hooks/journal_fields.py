"""Shared journal field reader and active-work-item lookup for Cursor hooks."""

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


def current_work_item_from_expert(text: str) -> str:
    return field(text, "Current work item")


def active_work_id(root: Path) -> str:
    """Work item id from active-context, legacy pointer, or expert journal."""
    context = root / ".cursor" / "active-context.txt"
    if context.is_file():
        lines = [line.strip() for line in read_text(context).splitlines() if line.strip()]
        if lines and lines[0].startswith("work-item:"):
            return lines[0].split(":", 1)[1].strip()
    pointer = root / ".cursor" / "active-work-item.txt"
    if pointer.is_file():
        lines = [line.strip() for line in read_text(pointer).splitlines() if line.strip()]
        if lines:
            return lines[0]
    expert = root / "journals" / "expert" / "progress.md"
    if expert.is_file():
        return current_work_item_from_expert(read_text(expert))
    return ""
