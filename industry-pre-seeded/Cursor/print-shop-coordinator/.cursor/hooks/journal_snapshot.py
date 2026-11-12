"""Commit the real journal paths for the audit trail."""

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


def _ensure_repo(root: Path) -> bool:
    inside = _git(root, "rev-parse", "--is-inside-work-tree")
    if inside.returncode == 0 and inside.stdout.strip() == "true":
        return True
    _log("No enclosing Git repository - initializing one for audit log...")
    init = _git(root, "init", "-q")
    if init.returncode != 0:
        _log("git init failed")
        return False
    _git(root, "config", "user.name", "Cursor Expert Agent")
    _git(root, "config", "user.email", "expert@cursor.local")
    gitignore = root / ".gitignore"
    if not gitignore.is_file():
        gitignore.write_text("__pycache__/\n*.pyc\n", encoding="utf-8")
    _git(root, "add", ".")
    _git(root, "commit", "-q", "-m", "Initial commit: Expert template baseline")
    return True


def _ignored(root: Path, path: Path) -> bool:
    rel = path.as_posix()
    try:
        rel = str(path.relative_to(root)).replace("\\", "/")
    except ValueError:
        return True
    check = _git(root, "check-ignore", "-q", rel)
    return check.returncode == 0


def _leaf_and_phase(state: dict) -> tuple[str, str]:
    active = state.get("active")
    if not isinstance(active, list) or not active:
        return "", "unknown"
    parts = [str(p).strip() for p in active if isinstance(p, str) and str(p).strip()]
    if not parts:
        return "", "unknown"
    return parts[-1], " / ".join(parts)


def snapshot_work_item(root: Path, work_id: str) -> int:
    if not work_id:
        _log("Empty Work Item ID - skipping audit log")
        return 0
    if not _ensure_repo(root):
        return 0

    journals_wi = root / "journals" / "work-items" / work_id
    status_path = root / "work-items" / work_id / "STATUS.md"
    attention = root / "work-items" / work_id / "NEEDS-ATTENTION.md"
    expert = root / "journals" / "expert" / "progress.md"
    state_path = journals_wi / "state.json"

    try:
        state = json.loads(read_text(state_path) or "{}") if state_path.is_file() else {}
    except json.JSONDecodeError:
        state = {}
    if not isinstance(state, dict):
        state = {}
    leaf, phase = _leaf_and_phase(state)
    node_path = journals_wi / "nodes" / f"{leaf}.md" if leaf else None
    next_action = "unknown"
    last_completed = "none"
    if node_path and node_path.is_file():
        node_text = read_text(node_path)
        next_action = field(node_text, "Next action") or "unknown"
        last_completed = field(node_text, "Last completed") or "none"

    commit_paths: list[str] = []
    for path in (expert, journals_wi, status_path, attention):
        if not path.exists():
            continue
        if _ignored(root, path):
            _log(f"{path} is gitignored - merged on disk, skipping commit path")
            continue
        try:
            rel = str(path.relative_to(root)).replace("\\", "/")
        except ValueError:
            continue
        commit_paths.append(rel)

    if not commit_paths:
        _log(f"No tracked journal paths for {work_id}")
        return 0

    # External absolute session: do not commit.
    if journals_wi.is_absolute() and root not in journals_wi.parents and journals_wi != root:
        _log(f"Session {work_id} is external - merged on disk, skipping git commit")
        return 0

    add = _git(root, "add", "--", *commit_paths)
    if add.returncode != 0:
        _log(f"git add failed: {add.stderr.strip()}")

    diff = _git(root, "diff", "--cached", "--quiet", "--", *commit_paths)
    if diff.returncode == 0:
        _log(f"No tracked journal changes to commit for {work_id}")
        return 0

    attention_tag = " [NEEDS-ATTENTION]" if attention.is_file() else ""
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    subject = f"WI-{work_id}: {phase} → {next_action}{attention_tag}"
    body = (
        f"{subject}\n\n"
        f"Phase:\n{phase}\n"
        f"Completed: {last_completed}\n"
        f"Next: {next_action}\n"
        f"Timestamp: {ts}\n"
    )
    commit = _git(root, "commit", "-q", "-m", body, "--", *commit_paths)
    if commit.returncode == 0:
        _log(f"Audit snapshot committed for WI-{work_id}: {phase} → {next_action}")
    else:
        _log("Failed to commit audit snapshot (may be no changes)")
    return 0


def snapshot_active(root: Path | None = None) -> int:
    root = root or Path.cwd()
    work_id = active_work_id(root)
    if not work_id:
        _log("No active Work Item - skipping audit log")
        return 0
    return snapshot_work_item(root, work_id)


def main() -> int:
    root = Path.cwd()
    if len(sys.argv) > 1:
        arg = Path(sys.argv[1])
        # Accept work-items/<id> or a bare id for convenience.
        wid = arg.name if arg.name != "work-items" else ""
        if arg.parts and arg.parts[0] == "work-items" and len(arg.parts) >= 2:
            wid = arg.parts[1]
        return snapshot_work_item(root, wid)
    return snapshot_active(root)


if __name__ == "__main__":
    raise SystemExit(main())
