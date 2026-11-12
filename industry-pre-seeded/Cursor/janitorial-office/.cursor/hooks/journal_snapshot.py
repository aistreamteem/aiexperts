"""Audit-commit the real journal paths for a work item."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

_HOOKS = Path(__file__).resolve().parent
if str(_HOOKS) not in sys.path:
    sys.path.insert(0, str(_HOOKS))

from journal_fields import active_leaf, active_work_id, field, read_text  # noqa: E402


def _run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=str(cwd),
        text=True,
        capture_output=True,
        check=False,
    )


def _inside_git(root: Path) -> bool:
    return _run(["git", "rev-parse", "--is-inside-work-tree"], root).returncode == 0


def _ignored(root: Path, path: Path) -> bool:
    rel = path.as_posix()
    try:
        rel = str(path.relative_to(root)).replace("\\", "/")
    except ValueError:
        return True
    return _run(["git", "check-ignore", "-q", rel], root).returncode == 0


def snapshot_work_item(root: Path, wid: str) -> None:
    if not wid:
        return
    if not _inside_git(root):
        print("No enclosing Git repository - skipping audit commit", file=sys.stderr)
        return

    journals = root / "journals" / "work-items" / wid
    status = root / "work-items" / wid / "STATUS.md"
    needs = root / "work-items" / wid / "NEEDS-ATTENTION.md"
    expert = root / "journals" / "expert" / "progress.md"

    state = {}
    state_path = journals / "state.json"
    try:
        raw = json.loads(read_text(state_path)) if state_path.is_file() else {}
        if isinstance(raw, dict):
            state = raw
    except json.JSONDecodeError:
        state = {}
    leaf = active_leaf(state)
    node_text = read_text(journals / "nodes" / f"{leaf}.md") if leaf else ""
    phase = "/".join(state.get("active") or []) if isinstance(state.get("active"), list) else ""
    next_action = field(node_text, "Next action") or "unknown"
    attention = " [NEEDS-ATTENTION]" if needs.is_file() else ""
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    commit_paths: list[Path] = []
    if expert.is_file():
        commit_paths.append(expert)
    if journals.is_dir():
        commit_paths.append(journals)
    if status.is_file():
        commit_paths.append(status)
    if needs.is_file():
        commit_paths.append(needs)

    rels: list[str] = []
    for path in commit_paths:
        if _ignored(root, path):
            print(f"Skipping gitignored path {path}", file=sys.stderr)
            continue
        try:
            rels.append(str(path.relative_to(root)).replace("\\", "/"))
        except ValueError:
            continue
    if not rels:
        print(f"No commit paths for {wid} (merge is on disk)", file=sys.stderr)
        return

    _run(["git", "add", "--"] + rels, root)
    diff = _run(["git", "diff", "--cached", "--quiet", "--"] + rels, root)
    if diff.returncode == 0:
        print(f"No tracked journal changes to commit for {wid}", file=sys.stderr)
        return

    subject = f"WI-{wid}: {phase or 'journal'} → {next_action}{attention}"
    body = (
        f"{subject}\n\n"
        f"Phase:\n{phase or 'unknown'}\n"
        f"Next: {next_action}\n"
        f"Timestamp: {ts}\n"
    )
    result = _run(["git", "commit", "-q", "-m", body, "--"] + rels, root)
    if result.returncode == 0:
        print(f"Audit snapshot committed for WI-{wid}: {phase} → {next_action}", file=sys.stderr)
    else:
        print("Failed to commit audit snapshot (may be no changes)", file=sys.stderr)


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    wid = ""
    if len(sys.argv) > 1 and sys.argv[1].strip():
        arg = sys.argv[1].strip().replace("\\", "/")
        if arg.startswith("work-items/"):
            wid = arg.split("/", 1)[1].strip("/")
        else:
            wid = Path(arg).name
    if not wid:
        wid = active_work_id(root)
    if not wid:
        print("No active Work Item - skipping audit log", file=sys.stderr)
        return 0
    snapshot_work_item(root, wid)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
