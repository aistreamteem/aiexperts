"""stop / subagentStop entry point: merge notes, refresh trigger index, emit {}."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
_HOOKS = Path(__file__).resolve().parent
if str(_HOOKS) not in sys.path:
    sys.path.insert(0, str(_HOOKS))


def _emit_empty() -> None:
    sys.stdout.write("{}\n")


def _should_skip(payload: dict) -> bool:
    active = str(payload.get("stop_hook_active", False)).lower() in {"true", "1"}
    try:
        loop = int(payload.get("loop_count") or 0)
    except (TypeError, ValueError):
        loop = 0
    return active or bool(loop)


def _rules_stale(index: Path, rules_glob: Path) -> bool:
    if not index.is_file():
        return True
    try:
        idx_mtime = index.stat().st_mtime
    except OSError:
        return True
    for rf in rules_glob.parent.glob(rules_glob.name):
        try:
            if rf.stat().st_mtime > idx_mtime:
                return True
        except OSError:
            continue
    return False


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

    try:
        from merge_agent_notes import main as merge_main

        merge_main()
    except Exception as exc:  # noqa: BLE001
        print(f"[on_stop] merge failed: {exc}", file=sys.stderr)

    gen = ROOT / "scripts" / "memory" / "build_trigger_index.py"
    idx = ROOT / "facts" / "trigger-index.json"
    if gen.is_file() and _rules_stale(idx, ROOT / "facts" / "rules-*.md"):
        subprocess.run(
            [sys.executable, str(gen)],
            cwd=str(ROOT),
            capture_output=True,
            check=False,
        )

    _emit_empty()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
