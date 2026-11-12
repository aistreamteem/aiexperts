"""stop / subagentStop entry point: merge notes, refresh trigger index, audit commit."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from journal_snapshot import snapshot
from merge_agent_notes import merge_all
from journal_fields import work_id


def _emit() -> None:
    sys.stdout.write("{}\n")


def _should_skip(payload: dict) -> bool:
    active = str(payload.get("stop_hook_active", False)).lower() in {"true", "1"}
    try:
        loop = int(payload.get("loop_count") or 0)
    except (TypeError, ValueError):
        loop = 0
    return active or bool(loop)


def _refresh_trigger_index(root: Path) -> None:
    gen = root / "scripts" / "memory" / "build_trigger_index.py"
    idx = root / "facts" / "trigger-index.json"
    if not gen.is_file():
        return
    stale = not idx.is_file()
    if not stale:
        idx_mtime = idx.stat().st_mtime
        for rf in (root / "facts").glob("rules-*.md"):
            if rf.stat().st_mtime > idx_mtime:
                stale = True
                break
    if stale:
        subprocess.run(
            [sys.executable, str(gen)],
            cwd=str(root),
            capture_output=True,
            check=False,
        )


def main() -> int:
    raw = sys.stdin.read()
    try:
        payload = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        payload = {}
    if not isinstance(payload, dict):
        payload = {}
    if _should_skip(payload):
        _emit()
        return 0
    root = Path.cwd()
    try:
        merged = merge_all(root)
        for wid in merged:
            snapshot(root, wid)
        if not merged:
            wid = work_id(root)
            if wid:
                snapshot(root, wid)
        _refresh_trigger_index(root)
    except Exception:
        pass
    _emit()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
