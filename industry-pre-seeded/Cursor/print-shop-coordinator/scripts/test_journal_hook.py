"""Cursor preToolUse journal hook loads the active branch only."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def _context(payload: dict) -> str:
    text = payload.get("additional_context") or ""
    nested = (payload.get("hookSpecificOutput") or {}).get("additionalContext") or ""
    _assert(bool(text), "additional_context missing")
    _assert(nested == text, "nested additionalContext drifted")
    _assert(payload.get("continue") is True, "continue was not true")
    return text


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _fill_field(text: str, name: str, value: str) -> str:
    pattern = re.compile(
        rf"^([ \t]*(?:[-*][ \t]+)?(?:\*){{0,2}}{re.escape(name)}(?:\*){{0,2}}[ \t]*:[ \t]*(?:\*){{0,2}}[ \t]*).*$",
        re.MULTILINE | re.IGNORECASE,
    )
    replaced, count = pattern.subn(rf"\g<1>{value}", text, count=1)
    if count:
        return replaced
    return text.rstrip() + f"\n\n**{name}:** {value}\n"


def _run_hook(payload: dict, workspace: Path) -> dict:
    hook = str(ROOT / ".cursor" / "hooks" / "inject_journal_context.py")
    completed = subprocess.run(
        [sys.executable, hook],
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        cwd=str(workspace),
        check=False,
    )
    _assert(completed.returncode == 0, completed.stderr or "hook failed")
    if not completed.stdout.strip():
        return {}
    return json.loads(completed.stdout)


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="cursor-journal-"))
    try:
        expert_src = ROOT / "journals" / "_TEMPLATE" / "expert" / "progress.md"
        wi_src = ROOT / "journals" / "work-items" / "_TEMPLATE"
        expert_dst = tmp / "journals" / "expert" / "progress.md"
        base = tmp / "journals" / "work-items" / "WID-1"
        shutil.copytree(wi_src, base)
        expert_text = _fill_field(
            expert_src.read_text(encoding="utf-8"), "Current work item", "WID-1"
        )
        _write(expert_dst, expert_text)
        progress = _fill_field(
            (base / "progress.md").read_text(encoding="utf-8"),
            "Completion status",
            "in progress",
        )
        (base / "progress.md").write_text(progress, encoding="utf-8")
        (base / "state.json").write_text(
            json.dumps(
                {
                    "active": ["work-item", "spec"],
                    "nodes": {
                        "work-item": {"parent": None, "status": "open", "history": []},
                        "spec": {"parent": "work-item", "status": "open", "history": []},
                        "implement": {"parent": "work-item", "status": "open", "history": []},
                    },
                }
            ),
            encoding="utf-8",
        )
        _write(base / "nodes" / "work-item.md", "ROOT_NOTE\n")
        _write(base / "nodes" / "spec.md", "ACTIVE_BRANCH_NOTE\n")
        _write(base / "nodes" / "implement.md", "INACTIVE_BRANCH_NOTE\n")
        (tmp / ".cursor").mkdir(parents=True, exist_ok=True)

        # No pointer files: work item comes from the expert journal line.
        body = _context(
            _run_hook(
                {"tool_name": "Bash", "tool_input": {"command": "echo hi"}},
                tmp,
            )
        )
        _assert("WID-1" in body, "expert journal / work item missing")
        _assert("ACTIVE_BRANCH_NOTE" in body, "active branch missing")
        _assert("INACTIVE_BRANCH_NOTE" not in body, "inactive branch was loaded")

        read_body = _context(
            _run_hook(
                {
                    "tool_name": "Read",
                    "tool_input": {
                        "file_path": "journals/work-items/WID-1/nodes/spec.md"
                    },
                },
                tmp,
            )
        )
        _assert(
            "ACTIVE_BRANCH_NOTE" not in read_body,
            "active note injected onto its own read",
        )
        _assert("WID-1" in read_body or "Work item" in read_body, "expert journal dropped")

        (base / "progress.md").write_text(
            _fill_field(progress, "Completion status", "done"),
            encoding="utf-8",
        )
        done_body = _context(
            _run_hook(
                {"tool_name": "Bash", "tool_input": {"command": "echo hi"}},
                tmp,
            )
        )
        _assert("ACTIVE_BRANCH_NOTE" not in done_body, "done branch note was loaded")
        _assert(
            "done" in done_body.lower() or "Completion status" in done_body,
            "done work item journal missing",
        )
        print("cursor journal hook tests passed")
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
