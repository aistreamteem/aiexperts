"""stop / subagentStop entry point. Always prints {} and exits 0."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from journal_fields import active_work_id
from journal_snapshot import snapshot
from merge_agent_notes import merge_all


def _payload() -> dict:
    raw = sys.stdin.read()
    try:
        data = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        data = {}
    return data if isinstance(data, dict) else {}


def _skip_merge(payload: dict) -> bool:
    active = str(payload.get("stop_hook_active", False)).lower() in {"true", "1"}
    try:
        loop = int(payload.get("loop_count") or 0)
    except (TypeError, ValueError):
        loop = 0
    return active or bool(loop)


def _trigger_index_stale(root: Path) -> bool:
    gen = root / "scripts" / "memory" / "build_trigger_index.py"
    idx = root / "facts" / "trigger-index.json"
    if not gen.is_file():
        return False
    if not idx.is_file():
        return True
    idx_mtime = idx.stat().st_mtime
    for rules in (root / "facts").glob("rules-*.md"):
        if rules.stat().st_mtime > idx_mtime:
            return True
    return False


def _refresh_trigger_index(root: Path) -> None:
    if not _trigger_index_stale(root):
        return
    import subprocess

    cmd = [sys.executable, str(root / "scripts" / "memory" / "build_trigger_index.py")]
    subprocess.run(cmd, cwd=str(root), capture_output=True, check=False)


def main() -> int:
    root = Path.cwd()
    payload = _payload()
    if not _skip_merge(payload):
        merged = merge_all(root)
        work_id = active_work_id(root)
        targets = list(dict.fromkeys([*merged, work_id] if work_id else merged))
        for wid in targets:
            if wid:
                snapshot(root, wid)
        _refresh_trigger_index(root)
    sys.stdout.write("{}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
