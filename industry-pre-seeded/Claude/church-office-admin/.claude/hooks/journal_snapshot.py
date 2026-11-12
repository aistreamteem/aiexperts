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


def _log(msg: str) -> None:
    print(f"[journal-snapshot] {msg}", file=sys.stderr)


def _git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=str(root),
        text=True,
        capture_output=True,
        check=False,
    )


def _inside_git(root: Path) -> bool:
    return _git(root, "rev-parse", "--is-inside-work-tree").returncode == 0


def _active_phase(state_path: Path) -> str:
    try:
        state = json.loads(read_text(state_path)) if state_path.is_file() else {}
    except json.JSONDecodeError:
        return "unknown"
    active = state.get("active") if isinstance(state, dict) else []
    if isinstance(active, list) and active:
        leaf = active[-1]
        if isinstance(leaf, str) and leaf.strip():
            return leaf.strip()
    return "unknown"


def snapshot_work_item(root: Path, work_id: str) -> None:
    if not work_id:
        return
    if not _inside_git(root):
        _log("no git repository - skipping audit commit")
        return

    journal_base = root / "journals" / "work-items" / work_id
    expert = root / "journals" / "expert" / "progress.md"
    status = root / "work-items" / work_id / "STATUS.md"
    needs = root / "work-items" / work_id / "NEEDS-ATTENTION.md"
    leaf = _active_phase(journal_base / "state.json")
    leaf_note = journal_base / "nodes" / f"{leaf}.md"
    next_action = field(read_text(leaf_note), "Next action") or "unknown"
    phase = leaf
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    paths: list[str] = []
    if expert.is_file():
        paths.append(str(expert.relative_to(root)).replace("\\", "/"))
    if journal_base.is_dir():
        paths.append(str(journal_base.relative_to(root)).replace("\\", "/"))
    if status.is_file():
        paths.append(str(status.relative_to(root)).replace("\\", "/"))
    if needs.is_file():
        paths.append(str(needs.relative_to(root)).replace("\\", "/"))
    if not paths:
        return

    # Skip commit when the journal tree is gitignored.
    check = _git(root, "check-ignore", "-q", str(journal_base / "progress.md"))
    if check.returncode == 0:
        _log(f"{work_id} journal is gitignored - merged on disk, skipping commit")
        return

    _git(root, "add", "--", *paths)
    staged = _git(root, "diff", "--cached", "--quiet", "--", *paths)
    if staged.returncode == 0:
        _log(f"no tracked journal changes to commit for {work_id}")
        return

    attention = ""
    if needs.is_file():
        attention = " [NEEDS-ATTENTION]"
    subject = f"WI-{work_id}: {phase} → {next_action}{attention}"
    body = (
        f"{subject}\n\n"
        f"Phase:\n{phase}\n"
        f"Next: {next_action}\n"
        f"Timestamp: {ts}\n"
    )
    commit = _git(root, "commit", "-q", "-m", body, "--", *paths)
    if commit.returncode == 0:
        _log(f"audit snapshot committed for WI-{work_id}: {phase} → {next_action}")
    else:
        _log(f"failed to commit audit snapshot for {work_id}")


def main() -> int:
    root = Path.cwd()
    work_id = sys.argv[1] if len(sys.argv) > 1 else active_work_id(root)
    if not work_id:
        _log("no active work item - skipping")
        return 0
    snapshot_work_item(root, work_id)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
