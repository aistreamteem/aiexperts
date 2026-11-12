"""Commit an audit snapshot of the real journals for one work item."""

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
    result = _run(["git", "check-ignore", "-q", str(path)], root)
    return result.returncode == 0


def _active_phase(state_path: Path) -> str:
    if not state_path.is_file():
        return "unknown"
    try:
        state = json.loads(read_text(state_path) or "{}")
    except json.JSONDecodeError:
        return "unknown"
    active = state.get("active") if isinstance(state, dict) else None
    if not isinstance(active, list) or not active:
        return "unknown"
    leaf = active[-1]
    return str(leaf) if leaf else "unknown"


def snapshot_work_item(root: Path, wid: str) -> None:
    if not wid:
        return
    if not _inside_git(root):
        _log("no git repository - skip audit commit")
        return

    journals_wi = root / "journals" / "work-items" / wid
    expert = root / "journals" / "expert" / "progress.md"
    status = root / "work-items" / wid / "STATUS.md"
    needs = root / "work-items" / wid / "NEEDS-ATTENTION.md"
    state_path = journals_wi / "state.json"
    leaf = _active_phase(state_path)
    leaf_path = journals_wi / "nodes" / f"{leaf}.md"
    next_action = field(read_text(leaf_path), "Next action") or "unknown"
    phase = leaf or "unknown"
    attention = " [NEEDS-ATTENTION]" if needs.is_file() else ""
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S%z")

    paths: list[Path] = []
    if expert.is_file():
        paths.append(expert)
    if journals_wi.is_dir():
        paths.append(journals_wi)
    if status.is_file():
        paths.append(status)
    if needs.is_file():
        paths.append(needs)

    # Skip commit when the journal tree is gitignored.
    if journals_wi.is_dir() and _ignored(root, journals_wi / "progress.md"):
        _log(f"{wid} journal is gitignored - merged on disk, skip commit")
        return

    rels = [str(p.relative_to(root)).replace("\\", "/") for p in paths]
    if not rels:
        return
    add = _run(["git", "add", "--", *rels], root)
    if add.returncode != 0:
        _log(f"git add failed for {wid}")
        return
    diff = _run(["git", "diff", "--cached", "--quiet", "--", *rels], root)
    if diff.returncode == 0:
        _log(f"no tracked journal changes to commit for {wid}")
        return
    subject = f"WI-{wid}: {phase} → {next_action}{attention}"
    body = (
        f"{subject}\n\n"
        f"Phase:\n{phase}\n"
        f"Next: {next_action}\n"
        f"Timestamp: {ts}\n"
    )
    commit = _run(["git", "commit", "-q", "-m", body, "--", *rels], root)
    if commit.returncode == 0:
        _log(f"audit snapshot committed for WI-{wid}: {phase} → {next_action}")
    else:
        _log(f"failed to commit audit snapshot for {wid}")


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    arg = sys.argv[1] if len(sys.argv) > 1 else ""
    if arg:
        wid = Path(arg).name
    else:
        wid = active_work_id(root)
    if not wid:
        _log("no active Work Item - skipping audit log")
        return 0
    snapshot_work_item(root, wid)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
