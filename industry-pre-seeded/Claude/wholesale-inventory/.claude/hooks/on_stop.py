"""stop / subagentStop entry point.

Merges pending agent notes, refreshes the trigger index when stale, always
prints {} and exits 0. Skips merge when a stop hook is already active.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _run_py(script: Path, *args: str) -> None:
    cmd = [sys.executable, str(script), *args]
    subprocess.run(cmd, cwd=str(ROOT), check=False)


def _should_skip(payload: dict) -> bool:
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
    for rf in (root / "facts").glob("rules-*.md"):
        if rf.stat().st_mtime > idx_mtime:
            return True
    return False


def main() -> int:
    raw = sys.stdin.read()
    try:
        payload = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        payload = {}
    if not isinstance(payload, dict):
        payload = {}

    if not _should_skip(payload):
        merge = ROOT / ".claude" / "hooks" / "merge_agent_notes.py"
        if merge.is_file():
            _run_py(merge)

        if _trigger_index_stale(ROOT):
            gen = ROOT / "scripts" / "memory" / "build_trigger_index.py"
            _run_py(gen)

    sys.stdout.write("{}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
