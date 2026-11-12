"""Cursor preToolUse journal hook loads the active branch only."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOOK = ROOT / ".claude" / "hooks" / "inject_journal_context.py"


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def _context(stdout: str) -> str:
    payload = json.loads(stdout)
    text = payload.get("additional_context") or ""
    nested = (payload.get("hookSpecificOutput") or {}).get("additionalContext") or ""
    _assert(bool(text), "additional_context missing")
    _assert(nested == text, "nested additionalContext drifted")
    _assert(payload.get("continue") is True, "continue was not true")
    return text


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _run_hook(payload: dict, workspace: Path) -> str:
    completed = subprocess.run(
        [sys.executable, str(HOOK)],
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        cwd=str(workspace),
        check=False,
    )
    _assert(completed.returncode == 0, completed.stderr or completed.stdout or "hook failed")
    return completed.stdout


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="cursor-journal-"))
    try:
        expert_tmpl = (ROOT / "journals" / "_TEMPLATE" / "expert" / "progress.md").read_text(
            encoding="utf-8"
        )
        wi_tmpl = (ROOT / "journals" / "work-items" / "_TEMPLATE" / "progress.md").read_text(
            encoding="utf-8"
        )
        state_tmpl = (ROOT / "journals" / "work-items" / "_TEMPLATE" / "state.json").read_text(
            encoding="utf-8"
        )
        node_tmpl = (
            ROOT / "journals" / "work-items" / "_TEMPLATE" / "nodes" / "work-item.md"
        ).read_text(encoding="utf-8")

        (tmp / ".claude").mkdir(parents=True, exist_ok=True)

        expert_text = expert_tmpl.replace(
            "**Current work item:**",
            "**Current work item:** WID-1",
            1,
        )
        _write(tmp / "journals" / "expert" / "progress.md", expert_text)

        base = tmp / "journals" / "work-items" / "WID-1"
        flat = wi_tmpl.replace(
            "**Completion status:** not started",
            "**Completion status:** in progress",
            1,
        )
        _write(base / "progress.md", flat)

        state = json.loads(state_tmpl)
        if not isinstance(state.get("active"), list) or len(state["active"]) < 2:
            state = {
                "active": ["work-item", "spec"],
                "nodes": {
                    "work-item": {"parent": None, "status": "open", "history": []},
                    "spec": {"parent": "work-item", "status": "open", "history": []},
                    "implement": {"parent": "work-item", "status": "open", "history": []},
                },
            }
        _write(base / "state.json", json.dumps(state, indent=2))
        leaf = state["active"][-1]
        _write(base / "nodes" / "work-item.md", "ROOT_NOTE\n" + node_tmpl)
        _write(base / "nodes" / f"{leaf}.md", "ACTIVE_BRANCH_NOTE\n")
        _write(base / "nodes" / "implement.md", "INACTIVE_BRANCH_NOTE\n")

        (tmp / ".claude" / "active-context.txt").write_text(
            "work-item:WID-1\n", encoding="utf-8"
        )

        body = _context(
            _run_hook({"tool_name": "Bash", "tool_input": {"command": "echo hi"}}, tmp)
        )
        _assert("WID-1" in body or "Work" in body or "Moving" in body or "Expert" in body, "expert journal missing")
        _assert("in progress" in body or "Completion status" in body, "work item journal missing")
        _assert("ACTIVE_BRANCH_NOTE" in body, "active branch missing")
        _assert("INACTIVE_BRANCH_NOTE" not in body, "inactive branch was loaded")

        read_body = _context(
            _run_hook(
                {
                    "tool_name": "Read",
                    "tool_input": {
                        "file_path": f"journals/work-items/WID-1/nodes/{leaf}.md"
                    },
                },
                tmp,
            )
        )
        _assert("ACTIVE_BRANCH_NOTE" not in read_body, "active note injected onto its own read")

        # No pointer files: resolve work item only from the expert journal line
        (tmp / ".claude" / "active-context.txt").unlink(missing_ok=True)
        (tmp / ".claude" / "active-work-item.txt").unlink(missing_ok=True)
        no_ptr_body = _context(
            _run_hook({"tool_name": "Bash", "tool_input": {"command": "echo hi"}}, tmp)
        )
        _assert("ACTIVE_BRANCH_NOTE" in no_ptr_body, "journal line did not resolve work item")

        # Done: edit the template's own Completion status line
        progress = (base / "progress.md").read_text(encoding="utf-8")
        progress = progress.replace(
            "**Completion status:** in progress",
            "**Completion status:** done",
            1,
        )
        (base / "progress.md").write_text(progress, encoding="utf-8")
        (tmp / ".claude" / "active-context.txt").write_text(
            "work-item:WID-1\n", encoding="utf-8"
        )
        done_body = _context(
            _run_hook({"tool_name": "Bash", "tool_input": {"command": "echo hi"}}, tmp)
        )
        _assert("ACTIVE_BRANCH_NOTE" not in done_body, "done branch note was loaded")
        _assert("done" in done_body.lower() or "Completion status" in done_body, "done journal missing")
        print("claude journal hook tests passed")
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
