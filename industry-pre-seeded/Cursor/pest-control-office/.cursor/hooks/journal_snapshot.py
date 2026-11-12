"""Audit commit for the real journals tree after a merge or journal update."""

from __future__ import annotations

import subprocess
from datetime import datetime, timezone
from pathlib import Path

from journal_fields import active_leaf, active_phase, field, read_text, work_id

ROOT = Path(__file__).resolve().parents[2]


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
    rel = str(path.relative_to(root)).replace("\\", "/")
    return _git(root, "check-ignore", "-q", rel).returncode == 0


def snapshot_work_item(root: Path, wid: str) -> None:
    if not wid or not _inside_git(root):
        return

    expert = root / "journals" / "expert" / "progress.md"
    journals = root / "journals" / "work-items" / wid
    status = root / "work-items" / wid / "STATUS.md"
    attention = root / "work-items" / wid / "NEEDS-ATTENTION.md"

    paths: list[Path] = []
    if expert.is_file():
        paths.append(expert)
    if journals.is_dir():
        paths.append(journals)
    if status.is_file():
        paths.append(status)
    if attention.is_file():
        paths.append(attention)

    # Skip commit when the journals tree is gitignored (still merged on disk).
    if journals.is_dir() and _ignored(root, journals):
        print(f"journals for {wid} gitignored - merged on disk, skipping commit")
        return

    rels = [str(p.relative_to(root)).replace("\\", "/") for p in paths]
    if not rels:
        return

    _git(root, "add", "--", *rels)
    staged = _git(root, "diff", "--cached", "--quiet", "--", *rels)
    if staged.returncode == 0:
        print(f"No tracked journal changes to commit for {wid}")
        return

    leaf = active_leaf(root, wid)
    node_text = ""
    if leaf:
        node_text = read_text(journals / "nodes" / f"{leaf}.md")
    phase = active_phase(root, wid) or "unknown"
    next_action = field(node_text, "Next action") or "unknown"
    attention_tag = " [NEEDS-ATTENTION]" if attention.is_file() else ""
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    subject = f"WI-{wid}: {phase} → {next_action}{attention_tag}"
    body = (
        f"{subject}\n\n"
        f"Phase:\n{phase}\n"
        f"Next: {next_action}\n"
        f"Timestamp: {ts}\n"
    )
    result = _git(root, "commit", "-q", "-m", body, "--", *rels)
    if result.returncode == 0:
        print(f"Audit snapshot committed for WI-{wid}: {phase} → {next_action}")
    else:
        print(f"Failed to commit audit snapshot for {wid}")


def main() -> int:
    root = ROOT
    wid = work_id(root)
    if not wid:
        print("No active Work Item - skipping audit log")
        return 0
    snapshot_work_item(root, wid)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
