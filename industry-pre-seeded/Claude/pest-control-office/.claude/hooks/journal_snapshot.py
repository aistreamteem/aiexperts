"""Commit an audit snapshot of the real journals for one work item."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from journal_fields import active_work_id, field, read_text

ROOT = Path(__file__).resolve().parents[2]


def log(msg: str) -> None:
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
    rel = path.as_posix()
    return _git(["check-ignore", "-q", rel]).returncode == 0


def _active_phase(wid: str) -> str:
    state_path = ROOT / "journals" / "work-items" / wid / "state.json"
    try:
        state = json.loads(read_text(state_path) or "{}")
    except json.JSONDecodeError:
        return "unknown"
    active = state.get("active") if isinstance(state, dict) else None
    if not isinstance(active, list) or not active:
        return "unknown"
    leaf = active[-1]
    return leaf if isinstance(leaf, str) and leaf.strip() else "unknown"


def snapshot_work_item(wid: str) -> int:
    if not wid:
        log("no work item - skipping audit log")
        return 0
    if not _inside_git():
        log("no enclosing Git repository - skipping audit commit")
        return 0

    journals_wi = ROOT / "journals" / "work-items" / wid
    expert = ROOT / "journals" / "expert" / "progress.md"
    status = ROOT / "work-items" / wid / "STATUS.md"
    attention = ROOT / "work-items" / wid / "NEEDS-ATTENTION.md"
    leaf = _active_phase(wid)
    node = journals_wi / "nodes" / f"{leaf}.md"
    node_text = read_text(node) if node.is_file() else ""
    next_action = field(node_text, "Next action") or "unknown"
    last_completed = field(node_text, "Last completed") or "none"
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    paths: list[Path] = []
    if expert.is_file():
        paths.append(expert)
    if journals_wi.is_dir():
        paths.append(journals_wi)
    if status.is_file():
        paths.append(status)
    if attention.is_file():
        paths.append(attention)

    # Skip commit when the whole journals tree is ignored; keep on-disk merge.
    sample = journals_wi / "progress.md"
    if sample.is_file() and _ignored(sample):
        log(f"Session {wid} is gitignored - merged on disk, skipping git commit")
        return 0

    rels = []
    for path in paths:
        rel = path.relative_to(ROOT).as_posix()
        rels.append(rel)
        _git(["add", "--", rel])

    staged = _git(["diff", "--cached", "--quiet", "--", *rels])
    if staged.returncode == 0:
        log(f"No tracked journal changes to commit for {wid}")
        return 0

    attention_tag = " [NEEDS-ATTENTION]" if attention.is_file() else ""
    subject = f"WI-{wid}: {leaf} → {next_action}{attention_tag}"
    body = (
        f"{subject}\n\n"
        f"Phase:\n{leaf}\n"
        f"Completed: {last_completed}\n"
        f"Next: {next_action}\n"
        f"Timestamp: {ts}\n"
    )
    result = _git(["commit", "-q", "-m", body, "--"] + rels)
    if result.returncode == 0:
        log(f"Audit snapshot committed for WI-{wid}: {leaf} → {next_action}")
    else:
        log("Failed to commit audit snapshot (may be no changes)")
    return 0


def main() -> int:
    wid = ""
    if len(sys.argv) > 1 and sys.argv[1].strip():
        arg = Path(sys.argv[1])
        wid = arg.name
    if not wid:
        wid = active_work_id(ROOT)
    return snapshot_work_item(wid)


if __name__ == "__main__":
    raise SystemExit(main())
