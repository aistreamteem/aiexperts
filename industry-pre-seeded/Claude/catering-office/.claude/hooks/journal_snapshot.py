"""Commit the real journal paths for the active work item (audit trail)."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from journal_fields import active_work_id, field, read_text

ROOT = Path(__file__).resolve().parents[2]


def _git(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=str(ROOT),
        text=True,
        capture_output=True,
        check=False,
    )


def _inside_git() -> bool:
    return _git(["rev-parse", "--is-inside-work-tree"]).returncode == 0


def _phase(work_id: str) -> str:
    state_path = ROOT / "journals" / "work-items" / work_id / "state.json"
    if not state_path.is_file():
        return ""
    try:
        state = json.loads(read_text(state_path))
    except json.JSONDecodeError:
        return ""
    active = state.get("active") if isinstance(state, dict) else None
    if isinstance(active, list) and active:
        leaf = active[-1]
        return str(leaf) if leaf is not None else ""
    return ""


def _next_action(work_id: str) -> str:
    leaf = _phase(work_id)
    if not leaf:
        return ""
    note = ROOT / "journals" / "work-items" / work_id / "nodes" / f"{leaf}.md"
    if note.is_file():
        return field(read_text(note), "Next action")
    return ""


def _ignored(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    result = _git(["check-ignore", "-q", rel])
    return result.returncode == 0


def snapshot_work_item(work_id: str) -> None:
    if not work_id or not _inside_git():
        return
    paths = [
        ROOT / "journals" / "expert" / "progress.md",
        ROOT / "journals" / "work-items" / work_id,
        ROOT / "work-items" / work_id / "STATUS.md",
        ROOT / "work-items" / work_id / "NEEDS-ATTENTION.md",
    ]
    to_add: list[str] = []
    for path in paths:
        if not path.exists():
            continue
        if path.is_file() and _ignored(path):
            continue
        to_add.append(str(path.relative_to(ROOT).as_posix()))
    if not to_add:
        return
    add = _git(["add", "--"] + to_add)
    if add.returncode != 0:
        return
    phase = _phase(work_id)
    next_action = _next_action(work_id)
    subject = f"WI-{work_id}: {phase} → {next_action or 'see the active node note'}"
    _git(["commit", "-m", subject, "--"] + to_add)


def main() -> int:
    work_id = active_work_id(ROOT)
    if work_id:
        snapshot_work_item(work_id)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
