"""Commit an audit snapshot of the real journal paths for one work item."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

_HOOKS = Path(__file__).resolve().parent
if str(_HOOKS) not in sys.path:
    sys.path.insert(0, str(_HOOKS))

from journal_fields import active_work_id, field, read_text  # noqa: E402


def _run(root: Path, args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=str(root),
        text=True,
        capture_output=True,
        check=False,
    )


def _ensure_git(root: Path) -> bool:
    inside = _run(root, ["git", "rev-parse", "--is-inside-work-tree"])
    if inside.returncode == 0 and inside.stdout.strip() == "true":
        return True
    init = _run(root, ["git", "init", "-q"])
    if init.returncode != 0:
        return False
    _run(root, ["git", "config", "user.name", "Cursor Expert Agent"])
    _run(root, ["git", "config", "user.email", "expert@cursor.local"])
    return True


def _active_phase(root: Path, work_id: str) -> str:
    state_path = root / "journals" / "work-items" / work_id / "state.json"
    try:
        state = json.loads(read_text(state_path) or "{}")
    except json.JSONDecodeError:
        return "unknown"
    active = state.get("active") if isinstance(state, dict) else None
    if isinstance(active, list) and active:
        leaf = active[-1]
        if isinstance(leaf, str) and leaf.strip():
            return leaf.strip()
    return "unknown"


def _leaf_next_action(root: Path, work_id: str, phase: str) -> str:
    note = root / "journals" / "work-items" / work_id / "nodes" / f"{phase}.md"
    if note.is_file():
        value = field(read_text(note), "Next action")
        if value:
            return value
    flat = root / "journals" / "work-items" / work_id / "progress.md"
    return field(read_text(flat), "Next action") or "unknown"


def snapshot_work_item(root: Path, work_id: str) -> bool:
    if not work_id:
        return False
    if not _ensure_git(root):
        return False
    journals_wi = root / "journals" / "work-items" / work_id
    expert = root / "journals" / "expert" / "progress.md"
    status = root / "work-items" / work_id / "STATUS.md"
    needs = root / "work-items" / work_id / "NEEDS-ATTENTION.md"

    paths: list[str] = []
    if expert.is_file():
        paths.append(str(expert.relative_to(root)).replace("\\", "/"))
    if journals_wi.is_dir():
        paths.append(str(journals_wi.relative_to(root)).replace("\\", "/"))
    if status.is_file():
        paths.append(str(status.relative_to(root)).replace("\\", "/"))
    if needs.is_file():
        paths.append(str(needs.relative_to(root)).replace("\\", "/"))
    if not paths:
        return False

    # Skip commit when the journal tree is gitignored; merge still stands on disk.
    sample = journals_wi / "progress.md"
    if sample.is_file():
        ignored = _run(root, ["git", "check-ignore", "-q", str(sample)])
        if ignored.returncode == 0:
            print(f"journal for {work_id} is gitignored - skip commit", flush=True)
            return False

    _run(root, ["git", "add", "--", *paths])
    staged = _run(root, ["git", "diff", "--cached", "--quiet", "--", *paths])
    if staged.returncode == 0:
        print(f"No tracked journal changes to commit for {work_id}", flush=True)
        return False

    phase = _active_phase(root, work_id)
    next_action = _leaf_next_action(root, work_id, phase)
    attention = " [NEEDS-ATTENTION]" if needs.is_file() else ""
    ts = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")
    subject = f"WI-{work_id}: {phase} → {next_action}{attention}"
    body = (
        f"{subject}\n\n"
        f"Phase:\n{phase}\n"
        f"Next: {next_action}\n"
        f"Timestamp: {ts}\n"
    )
    commit = _run(root, ["git", "commit", "-q", "-m", body, "--", *paths])
    if commit.returncode == 0:
        print(f"Audit snapshot committed for WI-{work_id}: {phase} → {next_action}", flush=True)
        return True
    print(f"Failed to commit audit snapshot for {work_id}", flush=True)
    return False


def main() -> int:
    root = Path.cwd()
    wid = active_work_id(root)
    if not wid:
        print("No active Work Item - skipping audit log", flush=True)
        return 0
    snapshot_work_item(root, wid)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
