"""stop / subagentStop entry point: merge notes, refresh trigger index, emit {}."""

from __future__ import annotations

import json
import sys
from pathlib import Path

_HOOKS = Path(__file__).resolve().parent
if str(_HOOKS) not in sys.path:
    sys.path.insert(0, str(_HOOKS))


def _emit_empty() -> None:
    sys.stdout.write("{}\n")


def _truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).lower() in {"true", "1", "yes"}


def _should_skip_merge(payload: dict) -> bool:
    if _truthy(payload.get("stop_hook_active")):
        return True
    try:
        loop = int(payload.get("loop_count") or 0)
    except (TypeError, ValueError):
        loop = 0
    return loop > 0


def _trigger_index_stale(root: Path) -> bool:
    gen = root / "scripts" / "memory" / "build_trigger_index.py"
    idx = root / "facts" / "trigger-index.json"
    if not gen.is_file():
        return False
    if not idx.is_file():
        return True
    idx_mtime = idx.stat().st_mtime
    for rules in sorted((root / "facts").glob("rules-*.md")):
        if rules.stat().st_mtime > idx_mtime:
            return True
    return False


def _refresh_trigger_index(root: Path) -> None:
    if not _trigger_index_stale(root):
        return
    gen = root / "scripts" / "memory" / "build_trigger_index.py"
    try:
        import runpy

        runpy.run_path(str(gen), run_name="__not_main__")
    except Exception:  # noqa: BLE001
        try:
            import subprocess

            subprocess.run(
                [sys.executable, str(gen)],
                cwd=str(root),
                capture_output=True,
                check=False,
            )
        except Exception:  # noqa: BLE001
            pass


def main() -> int:
    raw = sys.stdin.read()
    try:
        payload = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        payload = {}
    if not isinstance(payload, dict):
        payload = {}

    if _should_skip_merge(payload):
        _emit_empty()
        return 0

    root = Path.cwd()
    try:
        from merge_agent_notes import merge_all

        merge_all(root)
    except Exception as exc:  # noqa: BLE001
        print(f"[on_stop] merge failed: {exc}", file=sys.stderr)

    try:
        _refresh_trigger_index(root)
    except Exception as exc:  # noqa: BLE001
        print(f"[on_stop] trigger index refresh failed: {exc}", file=sys.stderr)

    _emit_empty()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
