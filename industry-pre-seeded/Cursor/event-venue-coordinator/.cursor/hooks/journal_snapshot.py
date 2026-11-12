"""Commit an audit snapshot of the real journal paths for one work item."""

from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from journal_fields import active_work_id, field, read_text


def _run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=str(cwd),
        text=True,
        capture_output=True,
        check=False,
    )


def _inside_git(root: Path) -> bool:
    result = _run(["git", "rev-parse", "--is-inside-work-tree"], root)
    return result.returncode == 0 and result.stdout.strip() == "true"


def _ignored(root: Path, path: Path) -> bool:
    rel = path.as_posix()
    result = _run(["git", "check-ignore", "-q", rel], root)
    return result.returncode == 0


def _phase_and_next(root: Path, work_id: str) -> tuple[str, str]:
    state_path = root / "journals" / "work-items" / work_id / "state.json"
    phase = "unknown"
    try:
        state = json.loads(read_text(state_path)) if state_path.is_file() else {}
    except json.JSONDecodeError:
        state = {}
    active = state.get("active") if isinstance(state, dict) else []
    if isinstance(active, list) and active:
        leaf = str(active[-1])
        phase = leaf
        note = root / "journals" / "work-items" / work_id / "nodes" / f"{leaf}.md"
        nxt = field(read_text(note), "Next action") if note.is_file() else ""
    else:
        nxt = ""
    flat = root / "journals" / "work-items" / work_id / "progress.md"
    if not nxt and flat.is_file():
        nxt = field(read_text(flat), "Next action")
    return phase or "unknown", nxt or "unknown"


def snapshot(root: Path, work_id: str | None = None) -> int:
    work_id = (work_id or active_work_id(root) or "").strip()
    if not work_id:
        print("No active Work Item - skipping audit log")
        return 0
    if not _inside_git(root):
        print("No enclosing Git repository - skipping audit commit")
        return 0

    journal_root = root / "journals" / "work-items" / work_id
    expert = root / "journals" / "expert" / "progress.md"
    status = root / "work-items" / work_id / "STATUS.md"
    needs = root / "work-items" / work_id / "NEEDS-ATTENTION.md"
    paths: list[Path] = []
    if expert.is_file():
        paths.append(expert)
    if journal_root.is_dir():
        paths.append(journal_root)
    if status.is_file():
        paths.append(status)
    if needs.is_file():
        paths.append(needs)

    if not paths:
        print(f"No journal paths for {work_id} - skipping audit log")
        return 0

    if any(_ignored(root, path) for path in paths if path.exists()):
        print(f"Journal for {work_id} is gitignored - merged on disk, skipping commit")
        return 0

    rels = [path.relative_to(root).as_posix() for path in paths]
    _run(["git", "add", "--"] + rels, root)
    staged = _run(["git", "diff", "--cached", "--quiet", "--"] + rels, root)
    if staged.returncode == 0:
        print(f"No tracked journal changes to commit for {work_id}")
        return 0

    phase, nxt = _phase_and_next(root, work_id)
    attention = ""
    if needs.is_file():
        attention = " [NEEDS-ATTENTION]"
    ts = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")
    message = (
        f"WI-{work_id}: {phase} → {nxt}{attention}\n\n"
        f"Phase:\n{phase}\n"
        f"Next: {nxt}\n"
        f"Timestamp: {ts}"
    )
    commit = _run(["git", "commit", "-q", "-m", message, "--"] + rels, root)
    if commit.returncode == 0:
        print(f"Audit snapshot committed for WI-{work_id}: {phase} → {nxt}")
    else:
        print("Failed to commit audit snapshot (may be no changes)")
    return 0


def main() -> int:
    import sys

    root = Path.cwd()
    work_id = sys.argv[1] if len(sys.argv) > 1 else None
    if work_id and work_id.startswith("work-items/"):
        work_id = Path(work_id).name
    return snapshot(root, work_id)


if __name__ == "__main__":
    raise SystemExit(main())
