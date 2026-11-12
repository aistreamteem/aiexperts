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

from journal_fields import field, read_text, work_id  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]


def _log(msg: str) -> None:
    print(f"[journal-snapshot] {msg}", file=sys.stderr)


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


def _active_phase(wid: str) -> str:
    state_path = ROOT / "journals" / "work-items" / wid / "state.json"
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


def _next_action(wid: str, phase: str) -> str:
    note = ROOT / "journals" / "work-items" / wid / "nodes" / f"{phase}.md"
    if note.is_file():
        value = field(read_text(note), "Next action")
        if value:
            return value
    return "unknown"


def snapshot_work_item(wid: str) -> bool:
    if not wid:
        return False
    if not _inside_git():
        _log("not inside a git work tree - skip commit (merge is on disk)")
        return False

    expert = ROOT / "journals" / "expert" / "progress.md"
    journals = ROOT / "journals" / "work-items" / wid
    status = ROOT / "work-items" / wid / "STATUS.md"
    needs = ROOT / "work-items" / wid / "NEEDS-ATTENTION.md"

    paths: list[str] = []
    for path in (expert, journals, status, needs):
        if path.exists():
            rel = path.relative_to(ROOT).as_posix()
            # Skip if gitignored
            ignored = _git(["check-ignore", "-q", rel])
            if ignored.returncode == 0:
                _log(f"{rel} is gitignored - leave on disk only")
                continue
            paths.append(rel)
    if not paths:
        _log(f"no commit paths for {wid}")
        return False

    # Stage only our paths.
    _git(["add", "--", *paths])
    staged = _git(["diff", "--cached", "--quiet", "--", *paths])
    if staged.returncode == 0:
        _log(f"no tracked journal changes to commit for {wid}")
        return False

    phase = _active_phase(wid)
    next_action = _next_action(wid, phase)
    attention = ""
    if needs.is_file():
        attention = " [NEEDS-ATTENTION]"
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    subject = f"WI-{wid}: {phase} → {next_action}{attention}"
    body = (
        f"{subject}\n\n"
        f"Phase:\n{phase}\n"
        f"Next: {next_action}\n"
        f"Timestamp: {ts}\n"
    )
    commit = _git(["commit", "-m", body, "--", *paths])
    if commit.returncode != 0:
        _log(f"commit failed for {wid}: {commit.stderr.strip()}")
        return False
    _log(f"audit snapshot committed for WI-{wid}: {phase} → {next_action}")
    return True


def main() -> int:
    wid = ""
    if len(sys.argv) > 1 and sys.argv[1].strip():
        arg = sys.argv[1].strip()
        # Accept work-items/<id> or bare id
        wid = Path(arg).name if "work-items" in arg.replace("\\", "/") else arg
    if not wid:
        wid = work_id(ROOT)
    if not wid:
        _log("no active Work Item - skipping audit log")
        return 0
    snapshot_work_item(wid)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
