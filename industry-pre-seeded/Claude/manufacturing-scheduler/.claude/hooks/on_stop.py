"""stop / subagentStop entry point: merge notes, refresh trigger index, emit {{}}."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _emit_empty() -> None:
    sys.stdout.write("{}\n")


def _should_skip(payload: dict) -> bool:
    active = str(payload.get("stop_hook_active", False)).lower() in {"true", "1"}
    try:
        loop = int(payload.get("loop_count") or 0)
    except (TypeError, ValueError):
        loop = 0
    return active or bool(loop)


def _rules_stale(facts: Path, index: Path) -> bool:
    if not index.is_file():
        return True
    try:
        index_mtime = index.stat().st_mtime
    except OSError:
        return True
    for rules in facts.glob("rules-*.md"):
        try:
            if rules.stat().st_mtime > index_mtime:
                return True
        except OSError:
            continue
    return False


def _refresh_trigger_index() -> None:
    gen = ROOT / "scripts" / "memory" / "build_trigger_index.py"
    idx = ROOT / "facts" / "trigger-index.json"
    facts = ROOT / "facts"
    if not gen.is_file() or not facts.is_dir():
        return
    if not _rules_stale(facts, idx):
        return
    try:
        import runpy

        runpy.run_path(str(gen), run_name="__main__")
    except SystemExit:
        pass
    except Exception:
        pass


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

    # Ensure hook package imports resolve when invoked as a script path
    hooks_dir = Path(__file__).resolve().parent
    if str(hooks_dir) not in sys.path:
        sys.path.insert(0, str(hooks_dir))

    try:
        import merge_agent_notes
        import journal_snapshot

        merged = merge_agent_notes.merge_all()
        for wid in merged:
            journal_snapshot.snapshot(wid)
    except Exception as exc:  # noqa: BLE001 - stop hooks must never fail the agent
        print(f"[on_stop] merge/snapshot error: {exc}", file=sys.stderr)

    _refresh_trigger_index()
    _emit_empty()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

