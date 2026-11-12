"""stop / subagentStop entry point: merge notes, refresh trigger index, emit {}."""

from __future__ import annotations

import json
import sys
from pathlib import Path

# Allow running as `py -3 .claude/hooks/on_stop.py` from the expert root.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from merge_agent_notes import main as merge_main  # noqa: E402


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
    data = _payload()
    root = Path.cwd()
    if not _skip_merge(data):
        try:
            merge_main()
        except Exception as exc:  # noqa: BLE001 - stop hooks must not fail the turn
            print(f"[on-stop] merge failed: {exc}", file=sys.stderr)
        try:
            _refresh_trigger_index(root)
        except Exception as exc:  # noqa: BLE001
            print(f"[on-stop] trigger refresh failed: {exc}", file=sys.stderr)
    sys.stdout.write("{}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
