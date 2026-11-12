"""stop and subagentStop hook.

Merges pending agent notes (journals/work-items/<id>/agent-notes/ into the
active node) and refreshes facts/trigger-index.json when a rules file is newer.
Stdout is always `{}` and the exit code is always 0, so this cannot loop the agent.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import merge_agent_notes  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]


def _skip_merge(raw: str) -> bool:
    try:
        data = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        data = {}
    if not isinstance(data, dict):
        return False
    active = str(data.get("stop_hook_active", False)).lower() in {"true", "1"}
    try:
        loop = int(data.get("loop_count") or 0)
    except (TypeError, ValueError):
        loop = 0
    return active or bool(loop)


def refresh_trigger_index(root: Path) -> None:
    generator = root / "scripts" / "memory" / "build_trigger_index.py"
    index = root / "facts" / "trigger-index.json"
    if not generator.is_file():
        return
    stale = not index.is_file()
    if not stale:
        built = index.stat().st_mtime
        stale = any(rule.stat().st_mtime > built for rule in (root / "facts").glob("rules-*.md"))
    if stale:
        subprocess.run(
            [sys.executable, str(generator)],
            cwd=str(root),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )


def main(root: Path | None = None) -> int:
    root = root or ROOT
    try:
        raw = sys.stdin.read() if not sys.stdin.isatty() else ""
        if _skip_merge(raw):
            print("{}")
            return 0
        merge_agent_notes.main(root)
        refresh_trigger_index(root)
    except Exception as exc:  # never fail a hook
        print(f"[on-stop] {exc}", file=sys.stderr)
    print("{}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
