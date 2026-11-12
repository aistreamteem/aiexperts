"""stop / subagentStop entry: merge agent notes, refresh trigger index, emit {}."""

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

    root = Path.cwd()
    if not (root / ".cursor").is_dir():
        root = ROOT

    hooks = Path(__file__).resolve().parent
    if str(hooks) not in sys.path:
        sys.path.insert(0, str(hooks))

    try:
        import merge_agent_notes

        merge_agent_notes.main()
    except Exception as exc:  # noqa: BLE001 — stop hooks must never fail the agent
        print(f"[on_stop] merge failed: {exc}", file=sys.stderr)

    try:
        _refresh_trigger_index(root)
    except Exception as exc:  # noqa: BLE001
        print(f"[on_stop] trigger refresh failed: {exc}", file=sys.stderr)

    _emit()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
