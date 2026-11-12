"""stop / subagentStop entry point: merge notes, refresh trigger index, emit {}."""

from __future__ import annotations

import json
import sys
from pathlib import Path

_HOOKS = Path(__file__).resolve().parent
if str(_HOOKS) not in sys.path:
    sys.path.insert(0, str(_HOOKS))

from merge_agent_notes import merge_all  # noqa: E402


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

    subprocess.run(
        [sys.executable, str(gen)],
        cwd=str(root),
        capture_output=True,
        check=False,
    )


def main() -> int:
    root = Path.cwd()
    data = _payload()
    event = str(data.get("hook_event_name") or data.get("event") or "").lower()
    # subagentStop always merges; stop skips when already in a stop-hook loop.
    if "subagent" not in event and _skip_merge(data):
        print("{}")
        return 0
    try:
        merge_all(root)
    except Exception:  # noqa: BLE001
        pass
    try:
        _refresh_trigger_index(root)
    except Exception:  # noqa: BLE001
        pass
    print("{}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
