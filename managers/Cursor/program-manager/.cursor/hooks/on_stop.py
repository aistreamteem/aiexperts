"""Stop and SubagentStop entry point.

Merges agent notes, then rebuilds the trigger index when any rules file is newer.
Always exits 0 and prints {} for Cursor stop hooks.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path.cwd()
sys.path.insert(0, str(Path(__file__).resolve().parent))


def _should_skip(payload: dict) -> bool:
    value = payload.get("stop_hook_active")
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"true", "1", "yes"}
    return False


def _rebuild_trigger_index_if_stale() -> None:
    generator = ROOT / "scripts" / "memory" / "build_trigger_index.py"
    index = ROOT / "facts" / "trigger-index.json"
    if not generator.is_file():
        return
    stale = not index.is_file()
    if not stale:
        index_mtime = index.stat().st_mtime
        for rules in sorted((ROOT / "facts").glob("rules-*.md")):
            if rules.stat().st_mtime > index_mtime:
                stale = True
                break
    if not stale:
        return
    subprocess.run(
        [sys.executable, str(generator)],
        cwd=str(ROOT),
        check=False,
        capture_output=True,
    )


def main() -> int:
    raw = sys.stdin.read()
    try:
        payload = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        payload = {}
    if not isinstance(payload, dict):
        payload = {}
    if not _should_skip(payload):
        from merge_agent_notes import main as merge_main  # noqa: E402

        merge_main()
        _rebuild_trigger_index_if_stale()
    json.dump({}, sys.stdout)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
