"""stop / subagentStop entry point: merge notes, refresh trigger index, emit {}."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

_HOOKS = Path(__file__).resolve().parent
if str(_HOOKS) not in sys.path:
    sys.path.insert(0, str(_HOOKS))

ROOT = Path(__file__).resolve().parents[2]


def _emit() -> None:
    sys.stdout.write("{}\n")
    sys.stdout.flush()


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
    stale = not idx.is_file()
    if not stale:
        idx_mtime = idx.stat().st_mtime
        for rules in (ROOT / "facts").glob("rules-*.md"):
            if rules.stat().st_mtime > idx_mtime:
                stale = True
                break
    if not stale:
        return
    subprocess.run(
        [sys.executable, str(gen)],
        cwd=str(ROOT),
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
    try:
        from merge_agent_notes import main as merge_main

        merge_main()
    except Exception as exc:  # noqa: BLE001
        print(f"[on_stop] merge failed: {exc}", file=sys.stderr)
    try:
        _refresh_trigger_index()
    except Exception as exc:  # noqa: BLE001
        print(f"[on_stop] trigger index refresh failed: {exc}", file=sys.stderr)
    _emit()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
