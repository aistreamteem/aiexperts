"""stop / subagentStop entry point: merge notes, audit commit, refresh triggers."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from journal_snapshot import snapshot
from merge_agent_notes import merge_all


def _emit() -> None:
    sys.stdout.write("{}\n")


def _skip_merge(payload: dict) -> bool:
    active = str(payload.get("stop_hook_active", False)).lower() in {"true", "1"}
    try:
        loop = int(payload.get("loop_count") or 0)
    except (TypeError, ValueError):
        loop = 0
    return active or bool(loop)


def _rules_stale(root: Path) -> bool:
    idx = root / "facts" / "trigger-index.json"
    gen = root / "scripts" / "memory" / "build_trigger_index.py"
    if not gen.is_file():
        return False
    if not idx.is_file():
        return True
    idx_mtime = idx.stat().st_mtime
    for rules in (root / "facts").glob("rules-*.md"):
        if rules.stat().st_mtime > idx_mtime:
            return True
    return False


def _refresh_triggers(root: Path) -> None:
    gen = root / "scripts" / "memory" / "build_trigger_index.py"
    if not gen.is_file():
        return
    if not _rules_stale(root):
        return
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
    root = Path.cwd()
    try:
        if not _skip_merge(payload):
            merged = merge_all(root)
            for work_id in merged:
                snapshot(root, work_id)
            _refresh_triggers(root)
    except Exception as exc:  # noqa: BLE001 — stop hooks must never fail the session
        print(f"[on_stop] {exc}", file=sys.stderr)
    _emit()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
