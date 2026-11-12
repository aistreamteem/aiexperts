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
    return result.returncode == 0 and "true" in (result.stdout or "").lower()


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
    if isinstance(active, list) and active:
        leaf = active[-1]
        if isinstance(leaf, str) and leaf.strip():
            return leaf.strip()
    return "unknown"


def snapshot_work_item(root: Path, wid: str) -> bool:
    if not wid or wid in {"_TEMPLATE", "_template"}:
        return False
    if not _inside_git(root):
        print(f"No enclosing Git repository - skipping audit commit for {wid}", file=sys.stderr)
        return False

    journals = root / "journals" / "work-items" / wid
    expert = root / "journals" / "expert" / "progress.md"
    status = root / "work-items" / wid / "STATUS.md"
    attention = root / "work-items" / wid / "NEEDS-ATTENTION.md"
    state_path = journals / "state.json"
    leaf = _active_phase(state_path)
    leaf_note = journals / "nodes" / f"{leaf}.md"
    next_action = field(read_text(leaf_note), "Next action") if leaf_note.is_file() else ""
    if not next_action:
        next_action = field(read_text(journals / "progress.md"), "Next action") or "unknown"
    phase = leaf or "unknown"

    paths: list[Path] = []
    if expert.is_file():
        paths.append(expert)
    if journals.is_dir():
        paths.append(journals)
    if status.is_file():
        paths.append(status)
    if attention.is_file():
        paths.append(attention)

    commit_paths: list[str] = []
    for path in paths:
        if _ignored(root, path):
            continue
        commit_paths.append(str(path.relative_to(root)).replace("\\", "/"))
    if not commit_paths:
        print(f"Journal for {wid} is external/gitignored - merge on disk only", file=sys.stderr)
        return False

    _run(["git", "add", "--", *commit_paths], root)
    staged = _run(["git", "diff", "--cached", "--quiet", "--", *commit_paths], root)
    if staged.returncode == 0:
        print(f"No tracked journal changes to commit for {wid}", file=sys.stderr)
        return False

    tag = " [NEEDS-ATTENTION]" if attention.is_file() else ""
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    subject = f"WI-{wid}: {phase} → {next_action}{tag}"
    body = (
        f"{subject}\n\n"
        f"Phase:\n{phase}\n"
        f"Next: {next_action}\n"
        f"Timestamp: {ts}\n"
    )
    result = _run(["git", "commit", "-q", "-m", body, "--", *commit_paths], root)
    if result.returncode == 0:
        print(f"Audit snapshot committed for WI-{wid}: {phase} → {next_action}", file=sys.stderr)
        return True
    print(f"Failed to commit audit snapshot for {wid}", file=sys.stderr)
    return False


def main() -> int:
    root = Path.cwd()
    wid = ""
    if len(sys.argv) > 1 and sys.argv[1].strip():
        arg = Path(sys.argv[1])
        wid = arg.name if arg.name.startswith("WID-") or arg.name.startswith("wid-") else arg.name
        if (arg / "STATUS.md").exists() or arg.name:
            wid = arg.name
    if not wid:
        wid = active_work_id(root)
    if not wid:
        print("No active Work Item - skipping audit log", file=sys.stderr)
        return 0
    snapshot_work_item(root, wid)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
