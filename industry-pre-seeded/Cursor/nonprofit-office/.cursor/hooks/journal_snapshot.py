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


def _ignored(root: Path, path: Path) -> bool:
    rel = path.as_posix()
    try:
        rel = str(path.relative_to(root)).replace("\\", "/")
    except ValueError:
        return True
    return _git(root, "check-ignore", "-q", rel).returncode == 0


def _active_phase(root: Path, wid: str) -> str:
    state_path = root / "journals" / "work-items" / wid / "state.json"
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


def _next_action(root: Path, wid: str, phase: str) -> str:
    note = root / "journals" / "work-items" / wid / "nodes" / f"{phase}.md"
    if note.is_file():
        value = field(read_text(note), "Next action")
        if value:
            return value
    flat = read_text(root / "journals" / "work-items" / wid / "progress.md")
    return field(flat, "Next action") or "unknown"


def snapshot_work_item(root: Path, wid: str | None = None) -> int:
    wid = wid or work_id(root)
    if not wid:
        _log("No active Work Item - skipping audit log")
        return 0
    if not _inside_git(root):
        _log("No enclosing Git repository - skipping audit commit")
        return 0

    journals = root / "journals"
    expert = journals / "expert" / "progress.md"
    wi_dir = journals / "work-items" / wid
    status = root / "work-items" / wid / "STATUS.md"
    needs = root / "work-items" / wid / "NEEDS-ATTENTION.md"

    if not (wi_dir / "progress.md").is_file():
        _log(f"Journal not found for {wid} - skipping audit log")
        return 0

    paths: list[Path] = []
    if expert.is_file():
        paths.append(expert)
    if wi_dir.is_dir():
        paths.extend(sorted(p for p in wi_dir.rglob("*") if p.is_file()))
    if status.is_file():
        paths.append(status)
    if needs.is_file():
        paths.append(needs)

    commit_paths: list[str] = []
    for path in paths:
        if _ignored(root, path):
            continue
        try:
            rel = str(path.relative_to(root)).replace("\\", "/")
        except ValueError:
            continue
        commit_paths.append(rel)

    if not commit_paths:
        _log(f"Session {wid} is external/gitignored - skipping git commit")
        return 0

    phase = _active_phase(root, wid)
    next_action = _next_action(root, wid, phase)
    attention = " [NEEDS-ATTENTION]" if needs.is_file() else ""
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    subject = f"WI-{wid}: {phase} → {next_action}{attention}"
    body = (
        f"{subject}\n\n"
        f"Phase:\n{phase}\n"
        f"Next: {next_action}\n"
        f"Timestamp: {ts}\n"
    )

    add = _git(root, "add", "--", *commit_paths)
    if add.returncode != 0:
        _log(f"git add failed for {wid}")
        return 0
    diff = _git(root, "diff", "--cached", "--quiet", "--", *commit_paths)
    if diff.returncode == 0:
        _log(f"No tracked journal changes to commit for {wid}")
        return 0
    commit = _git(root, "commit", "-q", "-m", body, "--", *commit_paths)
    if commit.returncode == 0:
        _log(f"Audit snapshot committed for WI-{wid}: {phase} → {next_action}")
    else:
        _log("Failed to commit audit snapshot (may be no changes)")
    return 0


def main() -> int:
    root = Path.cwd()
    arg = sys.argv[1] if len(sys.argv) > 1 else ""
    wid = None
    if arg:
        candidate = Path(arg)
        name = candidate.name
        if name.startswith("WID-") or name.startswith("wid-"):
            wid = name
        elif candidate.parent.name.startswith("WID-"):
            wid = candidate.parent.name
    return snapshot_work_item(root, wid)


if __name__ == "__main__":
    raise SystemExit(main())
