"""stop / SubagentStop entry point: merge notes, refresh trigger index, print {}."""

from __future__ import annotations

import json
import subprocess
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


def _refresh_triggers(root: Path) -> None:
    gen = root / "scripts" / "memory" / "build_trigger_index.py"
    idx = root / "facts" / "trigger-index.json"
    if not gen.is_file():
        return
    stale = not idx.is_file()
    if not stale:
        try:
            idx_mtime = idx.stat().st_mtime
        except OSError:
            idx_mtime = 0
            stale = True
        for rules in (root / "facts").glob("rules-*.md"):
            try:
                if rules.stat().st_mtime > idx_mtime:
                    stale = True
                    break
            except OSError:
                continue
    if stale:
        subprocess.run(
            [sys.executable, str(gen)],
            cwd=str(root),
            check=False,
            capture_output=True,
        )


def main() -> int:
    root = Path.cwd()
    data = _payload()
    if not _skip_merge(data):
        merge = root / ".claude" / "hooks" / "merge_agent_notes.py"
        if merge.is_file():
            subprocess.run(
                [sys.executable, str(merge)],
                cwd=str(root),
                check=False,
            )
    _refresh_triggers(root)
    sys.stdout.write("{}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
