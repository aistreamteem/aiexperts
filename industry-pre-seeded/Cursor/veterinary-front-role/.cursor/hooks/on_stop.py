"""stop / subagentStop entry point: merge notes, refresh trigger index, emit {}."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def _emit_empty() -> None:
    sys.stdout.write("{}\n")


def _should_skip(payload: dict) -> bool:
    active = str(payload.get("stop_hook_active", False)).lower() in {"true", "1"}
    try:
        loop = int(payload.get("loop_count") or 0)
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
        try:
            idx_mtime = idx.stat().st_mtime
        except OSError:
            stale = True
            idx_mtime = 0
        if not stale:
            for rf in sorted((root / "facts").glob("rules-*.md")):
                try:
                    if rf.stat().st_mtime > idx_mtime:
                        stale = True
                        break
                except OSError:
                    continue
    if stale:
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
    if _should_skip(payload):
        _emit_empty()
        return 0
    root = Path.cwd()
    try:
        from merge_agent_notes import main as merge_main

        merge_main()
    except Exception as exc:  # noqa: BLE001
        print(f"[on_stop] merge failed: {exc}", file=sys.stderr)
    try:
        _refresh_trigger_index(root)
    except Exception as exc:  # noqa: BLE001
        print(f"[on_stop] trigger refresh failed: {exc}", file=sys.stderr)
    _emit_empty()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
