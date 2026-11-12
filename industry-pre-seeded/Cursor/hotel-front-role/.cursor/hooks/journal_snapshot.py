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


def _ignored(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    return _git(["check-ignore", "-q", rel]).returncode == 0


def _phase_and_next(wid: str) -> tuple[str, str]:
    base = ROOT / "journals" / "work-items" / wid
    state_path = base / "state.json"
    phase = "unknown"
    try:
        state = json.loads(read_text(state_path)) if state_path.is_file() else {}
    except json.JSONDecodeError:
        state = {}
    active = state.get("active") if isinstance(state, dict) else []
    if isinstance(active, list) and active:
        leaf = active[-1]
        if isinstance(leaf, str) and leaf.strip():
            phase = leaf.strip()
            note = base / "nodes" / f"{phase}.md"
            nxt = field(read_text(note), "Next action") if note.is_file() else ""
            if nxt:
                return phase, nxt
    flat = base / "progress.md"
    nxt = field(read_text(flat), "Next action") if flat.is_file() else ""
    return phase, nxt or "unknown"


def snapshot_work_item(wid: str) -> None:
    if not wid or wid.startswith("_"):
        return
    if not _inside_git():
        _log("not inside a git work tree - skip commit")
        return

    paths: list[Path] = [
        ROOT / "journals" / "expert" / "progress.md",
        ROOT / "journals" / "work-items" / wid,
        ROOT / "work-items" / wid / "STATUS.md",
        ROOT / "work-items" / wid / "NEEDS-ATTENTION.md",
    ]
    commit_paths: list[str] = []
    for path in paths:
        if not path.exists():
            continue
        if path.is_file() and _ignored(path):
            _log(f"{path} is gitignored - merge on disk only")
            continue
        commit_paths.append(str(path.relative_to(ROOT).as_posix()))
    if not commit_paths:
        return

    _git(["add", "--", *commit_paths])
    staged = _git(["diff", "--cached", "--quiet", "--", *commit_paths])
    if staged.returncode == 0:
        _log(f"no tracked journal changes for {wid}")
        return

    phase, nxt = _phase_and_next(wid)
    attention = ""
    if (ROOT / "work-items" / wid / "NEEDS-ATTENTION.md").is_file():
        attention = " [NEEDS-ATTENTION]"
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    subject = f"WI-{wid}: {phase} → {nxt}{attention}"
    body = f"Phase:\n{phase}\nNext: {nxt}\nTimestamp: {ts}\n"
    result = _git(["commit", "-q", "-m", subject, "-m", body, "--", *commit_paths])
    if result.returncode == 0:
        _log(f"audit snapshot committed for WI-{wid}: {phase} → {nxt}")
    else:
        _log(f"commit failed for {wid} (may be no changes)")


def main() -> int:
    wid = sys.argv[1] if len(sys.argv) > 1 else active_work_id(ROOT)
    if wid:
        snapshot_work_item(wid)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
