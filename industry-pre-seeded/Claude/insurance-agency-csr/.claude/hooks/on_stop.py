"""stop / subagentStop entry point: merge notes, refresh trigger index, emit {}."""

from __future__ import annotations

import json
import sys
from pathlib import Path

_HOOKS = Path(__file__).resolve().parent
if str(_HOOKS) not in sys.path:
    sys.path.insert(0, str(_HOOKS))


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
    script = root / "scripts" / "memory" / "build_trigger_index.py"
    try:
        import subprocess

        subprocess.run(
            [sys.executable, str(script)],
            cwd=str(root),
            capture_output=True,
            check=False,
        )
    except OSError:
        pass


def main() -> int:
    data = _payload()
    root = Path.cwd()
    if not _skip_merge(data):
        try:
            import merge_agent_notes

            merge_agent_notes.main()
        except Exception as exc:  # noqa: BLE001
            print(f"[on_stop] merge failed: {exc}", file=sys.stderr)
        _refresh_trigger_index(root)
    json.dump({}, sys.stdout)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
