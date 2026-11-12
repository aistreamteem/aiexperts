"""stop / subagentStop entry point: merge notes, refresh trigger index, emit {}."""

from __future__ import annotations

import json
import sys
from pathlib import Path


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
        for rf in (root / "facts").glob("rules-*.md"):
            if rf.stat().st_mtime > idx_mtime:
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
    root = Path(__file__).resolve().parents[2]
    data = _payload()
    if not _skip_merge(data):
        try:
            # Ensure hook package imports resolve when run as a script path
            sys.path.insert(0, str(Path(__file__).resolve().parent))
            import merge_agent_notes

            merge_agent_notes.main()
        except Exception as exc:  # noqa: BLE001
            print(f"[on_stop] merge failed: {exc}", file=sys.stderr)
        try:
            _refresh_trigger_index(root)
        except Exception as exc:  # noqa: BLE001
            print(f"[on_stop] trigger refresh failed: {exc}", file=sys.stderr)
    sys.stdout.write("{}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
