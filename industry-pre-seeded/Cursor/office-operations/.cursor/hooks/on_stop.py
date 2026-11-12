"""stop / subagentStop entry point: merge notes, refresh trigger index, emit {}."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def _run_py(root: Path, script: Path, stdin: str = "") -> None:
    subprocess.run(
        [sys.executable, str(script)],
        input=stdin,
        text=True,
        cwd=str(root),
        check=False,
        capture_output=True,
    )


def _should_skip_merge(payload: dict) -> bool:
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
        try:
            idx_mtime = idx.stat().st_mtime
        except OSError:
            stale = True
            idx_mtime = 0
        if not stale:
            for rules in (root / "facts").glob("rules-*.md"):
                try:
                    if rules.stat().st_mtime > idx_mtime:
                        stale = True
                        break
                except OSError:
                    continue
    if stale:
        _run_py(root, gen)


def main() -> int:
    raw = sys.stdin.read()
    try:
        payload = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        payload = {}
    if not isinstance(payload, dict):
        payload = {}
    root = Path.cwd()
    if not _should_skip_merge(payload):
        _run_py(root, root / ".cursor" / "hooks" / "merge_agent_notes.py")
        _refresh_trigger_index(root)
    sys.stdout.write("{}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
