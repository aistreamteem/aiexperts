"""Commit the real journal audit snapshot after merges."""

from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from journal_fields import active_work_id, field, read_text


def _run(root: Path, args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=str(root),
        text=True,
        capture_output=True,
        check=False,
    )


def _inside_git(root: Path) -> bool:
    return _run(root, ["git", "rev-parse", "--is-inside-work-tree"]).returncode == 0


def _active_phase(root: Path, work_id: str) -> str:
    state_path = root / "journals" / "work-items" / work_id / "state.json"
    if not state_path.is_file():
        return "unknown"
    try:
        state = json.loads(read_text(state_path))
    except json.JSONDecodeError:
        return "unknown"
    active = state.get("active") if isinstance(state, dict) else None
    if isinstance(active, list) and active:
        leaf = active[-1]
        if isinstance(leaf, str) and leaf.strip():
            return leaf.strip()
    return "unknown"


def _next_action(root: Path, work_id: str, phase: str) -> str:
    note = root / "journals" / "work-items" / work_id / "nodes" / f"{phase}.md"
    if note.is_file():
        value = field(read_text(note), "Next action")
        if value:
            return value
    flat = root / "journals" / "work-items" / work_id / "progress.md"
    if flat.is_file():
        value = field(read_text(flat), "Next action")
        if value:
            return value
    return "unknown"


def snapshot(root: Path | None = None, work_id: str | None = None) -> int:
    root = root or Path.cwd()
    work_id = work_id or active_work_id(root)
    if not work_id:
        return 0
    if not _inside_git(root):
        return 0

    journal_root = root / "journals" / "work-items" / work_id
    if not journal_root.is_dir():
        return 0

    paths = [
        "journals/expert/progress.md",
        f"journals/work-items/{work_id}",
        f"work-items/{work_id}/STATUS.md",
        f"work-items/{work_id}/NEEDS-ATTENTION.md",
    ]
    existing = [path for path in paths if (root / path).exists()]
    if not existing:
        return 0

    ignored = _run(root, ["git", "check-ignore", "-q", f"journals/work-items/{work_id}/progress.md"])
    if ignored.returncode == 0:
        return 0

    _run(root, ["git", "add", "--"] + existing)
    staged = _run(root, ["git", "diff", "--cached", "--quiet", "--"] + existing)
    if staged.returncode == 0:
        return 0

    phase = _active_phase(root, work_id)
    next_action = _next_action(root, work_id, phase)
    attention = ""
    if (root / "work-items" / work_id / "NEEDS-ATTENTION.md").is_file():
        attention = " [NEEDS-ATTENTION]"
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    message = (
        f"WI-{work_id}: {phase} → {next_action}{attention}\n\n"
        f"Phase:\n{phase}\n"
        f"Next: {next_action}\n"
        f"Timestamp: {ts}\n"
    )
    result = _run(root, ["git", "commit", "-q", "-m", message, "--"] + existing)
    return 0 if result.returncode == 0 else 0


def main() -> int:
    snapshot(Path.cwd())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
