"""stop / subagentStop entry point: merge notes, refresh trigger index, audit commit."""

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
    rules = list((root / "facts").glob("rules-*.md"))
    stale = not idx.is_file()
    if not stale and rules:
        idx_mtime = idx.stat().st_mtime
        stale = any(rf.stat().st_mtime > idx_mtime for rf in rules if rf.is_file())
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
    root = Path(__file__).resolve().parents[2]
    data = _payload()
    merged: list[str] = []
    if not _skip_merge(data):
        try:
            merged = merge_all(root)
        except Exception:
            merged = []
        try:
            _refresh_trigger_index(root)
        except Exception:
            pass
        for wid in merged:
            try:
                snapshot(root, wid)
            except Exception:
                pass
    sys.stdout.write("{}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
