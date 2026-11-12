"""stop / subagentStop entry point: merge notes, refresh trigger index, emit {}."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


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


def _run_merge() -> None:
    merge = ROOT / ".claude" / "hooks" / "merge_agent_notes.py"
    subprocess.run(
        [sys.executable, str(merge)],
        cwd=str(ROOT),
        check=False,
        capture_output=True,
        text=True,
    )


def _refresh_trigger_index() -> None:
    gen = ROOT / "scripts" / "memory" / "build_trigger_index.py"
    idx = ROOT / "facts" / "trigger-index.json"
    if not gen.is_file():
        return
    stale = not idx.is_file()
    if not stale:
        idx_mtime = idx.stat().st_mtime
        for rules in (ROOT / "facts").glob("rules-*.md"):
            if rules.stat().st_mtime > idx_mtime:
                stale = True
                break
    if stale:
        subprocess.run(
            [sys.executable, str(gen)],
            cwd=str(ROOT),
            check=False,
            capture_output=True,
            text=True,
        )


def main() -> int:
    data = _payload()
    if not _skip_merge(data):
        _run_merge()
        _refresh_trigger_index()
    sys.stdout.write("{}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
