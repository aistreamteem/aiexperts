"""Cursor stop / subagentStop entry point.

Merges pending agent notes, refreshes a stale trigger index, always prints {}
and exits 0. Skips the merge when a stop hook is already active.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from merge_agent_notes import main as merge_main


def _truthy(value: object) -> bool:
    return str(value).lower() in {"true", "1", "yes"}


def _should_skip(payload: dict) -> bool:
    if _truthy(payload.get("stop_hook_active", False)):
        return True
    try:
        loop = int(payload.get("loop_count") or 0)
    except (TypeError, ValueError):
        loop = 0
    return loop > 0


def _refresh_trigger_index(root: Path) -> None:
    gen = root / "scripts" / "memory" / "build_trigger_index.py"
    idx = root / "facts" / "trigger-index.json"
    if not gen.is_file():
        return
    stale = not idx.is_file()
    if not stale:
        idx_mtime = idx.stat().st_mtime
        for rules in (root / "facts").glob("rules-*.md"):
            if rules.stat().st_mtime > idx_mtime:
                stale = True
                break
    if not stale:
        return
    import subprocess

    cmd = [sys.executable, str(gen)]
    subprocess.run(cmd, cwd=str(root), capture_output=True, check=False)


def main() -> int:
    raw = sys.stdin.read()
    try:
        payload = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        payload = {}
    if not isinstance(payload, dict):
        payload = {}
    root = Path.cwd()
    if not _should_skip(payload):
        try:
            merge_main()
        except Exception:  # noqa: BLE001
            pass
        try:
            _refresh_trigger_index(root)
        except Exception:  # noqa: BLE001
            pass
    sys.stdout.write("{}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
