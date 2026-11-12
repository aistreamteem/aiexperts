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


def current_work_item(text: str) -> str:
    return field(text, "Current work item")


def work_id(root: Path, expert_text: str = "") -> str:
    context = root / ".cursor" / "active-context.txt"
    if context.is_file():
        lines = read_text(context).splitlines()
        line = lines[0].strip() if lines else ""
        if line.startswith("work-item:"):
            return line.split(":", 1)[1].strip()
    pointer = root / ".cursor" / "active-work-item.txt"
    if pointer.is_file():
        lines = [line.strip() for line in read_text(pointer).splitlines() if line.strip()]
        if lines:
            return lines[0]
    if not expert_text:
        expert_text = read_text(root / "journals" / "expert" / "progress.md")
    return current_work_item(expert_text)
