"""Stop / SubagentStop hook entry point (stdlib only).

Reads the hook JSON on stdin, merges pending background-agent notes, keeps the
trigger index in sync with facts/rules-*.md, prints `{}`, and ALWAYS exits 0.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import merge_agent_notes  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]


def index_is_stale(root: Path) -> bool:
    index = root / "facts" / "trigger-index.json"
    if not index.is_file():
        return True
    built = index.stat().st_mtime
    return any(p.stat().st_mtime > built for p in (root / "facts").glob("rules-*.md"))


def rebuild_index(root: Path) -> None:
    script = root / "scripts" / "memory" / "build_trigger_index.py"
    if not script.is_file() or not index_is_stale(root):
        return
    subprocess.run(
        [sys.executable, str(script)],
        cwd=str(root),
        capture_output=True,
        check=False,
        timeout=60,
    )


def _payload() -> dict:
    try:
        raw = sys.stdin.read()
        data = json.loads(raw) if raw.strip() else {}
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def run(root: Path, payload: dict) -> None:
    if payload.get("stop_hook_active") is True:
        return
    merge_agent_notes.main(root, log=lambda _message: None)
    try:
        rebuild_index(root)
    except Exception:
        pass


def main() -> int:
    try:
        run(ROOT, _payload())
    except Exception:
        pass
    print("{}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
