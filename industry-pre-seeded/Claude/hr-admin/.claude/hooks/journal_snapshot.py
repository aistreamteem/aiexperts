"""Audit-commit the real journal paths for the active (or named) work item."""

from __future__ import annotations

import subprocess
from pathlib import Path

from journal_fields import active_work_id, field, read_text


def _run(root: Path, args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=str(root),
        text=True,
        capture_output=True,
        check=False,
    )


def _inside_git(root: Path) -> bool:
    return _run(root, ["git", "rev-parse", "--is-inside-work-tree"]).returncode == 0


def _ignored(root: Path, path: Path) -> bool:
    rel = path.as_posix()
    try:
        rel = str(path.relative_to(root)).replace("\\", "/")
    except ValueError:
        return True
    return _run(root, ["git", "check-ignore", "-q", rel]).returncode == 0


def snapshot(root: Path, work_id: str | None = None) -> int:
    if not _inside_git(root):
        return 0
    wid = (work_id or active_work_id(root) or "").strip()
    if not wid:
        return 0

    journals = root / "journals" / "work-items" / wid
    expert = root / "journals" / "expert" / "progress.md"
    status = root / "work-items" / wid / "STATUS.md"
    needs = root / "work-items" / wid / "NEEDS-ATTENTION.md"
    flat = journals / "progress.md"
    state_path = journals / "state.json"

    if not flat.is_file() and not journals.is_dir():
        return 0

    # Phase from active path; next action from leaf node.
    phase = ""
    next_action = "unknown"
    last_completed = "none"
    try:
        import json

        state = json.loads(read_text(state_path) or "{}") if state_path.is_file() else {}
        active = state.get("active") if isinstance(state, dict) else []
        if isinstance(active, list) and active:
            phase = str(active[-1])
            leaf = journals / "nodes" / f"{phase}.md"
            if leaf.is_file():
                body = read_text(leaf)
                next_action = field(body, "Next action") or "unknown"
                last_completed = field(body, "Last completed") or "none"
    except Exception:
        pass
    if not phase:
        phase = field(read_text(flat), "Current phase") or "unknown"

    commit_paths: list[Path] = []
    if expert.is_file():
        commit_paths.append(expert)
    if journals.is_dir():
        commit_paths.append(journals)
    if status.is_file():
        commit_paths.append(status)
    if needs.is_file():
        commit_paths.append(needs)

    # Skip commit when the journal tree is gitignored.
    if journals.is_dir() and _ignored(root, journals):
        return 0

    rels: list[str] = []
    for path in commit_paths:
        try:
            rels.append(str(path.relative_to(root)).replace("\\", "/"))
        except ValueError:
            continue
    if not rels:
        return 0

    _run(root, ["git", "add", "--", *rels])
    staged = _run(root, ["git", "diff", "--cached", "--quiet", "--", *rels])
    if staged.returncode == 0:
        return 0

    attention = ""
    if needs.is_file():
        attention = " [NEEDS-ATTENTION]"
    subject = f"WI-{wid}: {phase} → {next_action}{attention}"
    body = (
        f"Phase:\n{phase}\nCompleted: {last_completed}\n"
        f"Next: {next_action}\n"
    )
    msg = f"{subject}\n\n{body}"
    _run(root, ["git", "commit", "-q", "-m", msg, "--", *rels])
    return 0


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    return snapshot(root)


if __name__ == "__main__":
    raise SystemExit(main())
