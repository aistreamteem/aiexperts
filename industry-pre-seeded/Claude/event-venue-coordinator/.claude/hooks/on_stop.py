"""stop / subagentStop entry point: merge notes, audit commit, refresh triggers."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from journal_snapshot import snapshot
from merge_agent_notes import merge_all


def _payload() -> dict:
    raw = sys.stdin.read()
    try:
        data = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        data = {}
    return data if isinstance(data, dict) else {}


def _skip_merge(data: dict) -> bool:
    active = str(data.get("stop_hook_active", False)).lower() in {"true", "1"}
    try:
        loop = int(data.get("loop_count") or 0)
    except (TypeError, ValueError):
        loop = 0
    return active or bool(loop)


def _refresh_trigger_index(root: Path) -> None:
    gen = root / "scripts" / "memory" / "build_trigger_index.py"
    idx = root / "facts" / "trigger-index.json"
    if not gen.is_file():
        return
    rules = sorted((root / "facts").glob("rules-*.md"))
    stale = not idx.is_file()
    if not stale and rules:
        idx_mtime = idx.stat().st_mtime
        stale = any(path.stat().st_mtime > idx_mtime for path in rules if path.is_file())
    if not stale:
        return
    import subprocess

    subprocess.run(
        [sys.executable, str(gen)],
        cwd=str(root),
        capture_output=True,
        check=False,
    )


def main() -> int:
    root = Path.cwd()
    data = _payload()
    if not _skip_merge(data):
        merged = merge_all(root)
        for work_id in merged:
            snapshot(root, work_id)
    _refresh_trigger_index(root)
    sys.stdout.write("{}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
