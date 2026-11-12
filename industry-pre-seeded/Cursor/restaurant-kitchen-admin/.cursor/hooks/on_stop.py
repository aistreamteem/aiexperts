"""stop / subagentStop entry point: merge notes, refresh trigger index, exit 0."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _emit() -> None:
    sys.stdout.write("{}\n")


def _should_skip(payload: dict) -> bool:
    active = str(payload.get("stop_hook_active", False)).lower() in {"true", "1"}
    try:
        loop = int(payload.get("loop_count") or 0)
    except (TypeError, ValueError):
        loop = 0
    return active or bool(loop)


def _refresh_trigger_index() -> None:
    gen = ROOT / "scripts" / "memory" / "build_trigger_index.py"
    idx = ROOT / "facts" / "trigger-index.json"
    if not gen.is_file():
        return
    rules = list((ROOT / "facts").glob("rules-*.md"))
    stale = not idx.is_file()
    if not stale and rules:
        idx_mtime = idx.stat().st_mtime
        stale = any(rule.stat().st_mtime > idx_mtime for rule in rules)
    if not stale:
        return
    import runpy

    try:
        runpy.run_path(str(gen), run_name="__main__")
    except SystemExit:
        pass
    except Exception:
        pass


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
    try:
        from merge_agent_notes import main as merge_main

        merge_main()
    except Exception:
        pass
    try:
        _refresh_trigger_index()
    except Exception:
        pass
    _emit()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
