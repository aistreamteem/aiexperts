"""Cursor preToolUse journal hook loads the active branch only."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOOK = ROOT / ".cursor" / "hooks" / "inject_journal_context.py"


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _run(payload: dict, workspace: Path) -> dict:
    completed = subprocess.run(
        [sys.executable, str(HOOK)],
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        cwd=str(workspace),
        check=False,
    )
    if completed.returncode != 0:
        raise SystemExit(completed.stderr or completed.stdout or "hook failed")
    if not completed.stdout.strip():
        return {}
    return json.loads(completed.stdout)


def _context(payload: dict) -> str:
    text = payload.get("additional_context") or ""
    nested = (payload.get("hookSpecificOutput") or {}).get("additionalContext") or ""
    _assert(bool(text), "additional_context missing")
    _assert(nested == text, "nested additionalContext drifted")
    _assert(payload.get("continue") is True, "continue was not true")
    return text


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

        (tmp / ".cursor").mkdir(parents=True, exist_ok=True)
        expert = tmp / "journals" / "expert" / "progress.md"
        expert_text = expert_tmpl
        if "**Current work item:**" in expert_text:
            expert_text = expert_text.replace(
                "**Current work item:**",
                "**Current work item:** WID-1",
                1,
            )
        else:
            expert_text += "\n**Current work item:** WID-1\n"
        _write(expert, expert_text)

        base = tmp / "journals" / "work-items" / "WID-1"
        wi_body = wi_tmpl.replace(
            "**Completion status:** not started",
            "**Completion status:** in progress",
            1,
        )
        _write(base / "progress.md", wi_body)

        state = json.loads(state_tmpl)
        state.setdefault("nodes", {})
        state["nodes"].setdefault(
            "work-item", {"parent": None, "status": "open", "history": []}
        )
        state["nodes"]["spec"] = {
            "parent": "work-item",
            "status": "open",
            "history": [],
        }
        state["nodes"]["implement"] = {
            "parent": "work-item",
            "status": "open",
            "history": [],
        }
        state["active"] = ["work-item", "spec"]
        _write(base / "state.json", json.dumps(state, indent=2))
        _write(base / "nodes" / "work-item.md", "ROOT_NOTE\n\n" + node_tmpl)
        _write(base / "nodes" / "spec.md", "ACTIVE_BRANCH_NOTE\n")
        _write(base / "nodes" / "implement.md", "INACTIVE_BRANCH_NOTE\n")

        (tmp / ".cursor" / "active-context.txt").write_text(
            "work-item:WID-1\n", encoding="utf-8"
        )
        loaded = _run(
            {"tool_name": "Bash", "tool_input": {"command": "echo hi"}},
            tmp,
        )
        body = _context(loaded)
        _assert("WID-1" in body or "Premise" in body or "Current work item" in body, "expert journal missing")
        _assert("ACTIVE_BRANCH_NOTE" in body, "active branch missing")
        _assert("INACTIVE_BRANCH_NOTE" not in body, "inactive branch was loaded")
        _assert("Workflow" in body or "Completion status" in body or "in progress" in body, "work item journal missing")

        reading = _run(
            {
                "tool_name": "Read",
                "tool_input": {"file_path": "journals/work-items/WID-1/nodes/spec.md"},
            },
            tmp,
        )
        read_body = _context(reading)
        _assert("ACTIVE_BRANCH_NOTE" not in read_body, "active note injected onto its own read")

        (tmp / ".cursor" / "active-context.txt").unlink(missing_ok=True)
        (tmp / ".cursor" / "active-work-item.txt").unlink(missing_ok=True)
        from_journal = _run(
            {"tool_name": "Bash", "tool_input": {"command": "echo hi"}},
            tmp,
        )
        from_body = _context(from_journal)
        _assert("ACTIVE_BRANCH_NOTE" in from_body, "work item not found from expert journal")

        done_text = (base / "progress.md").read_text(encoding="utf-8").replace(
            "**Completion status:** in progress",
            "**Completion status:** done",
            1,
        )
        (base / "progress.md").write_text(done_text, encoding="utf-8")
        (tmp / ".cursor" / "active-context.txt").write_text(
            "work-item:WID-1\n", encoding="utf-8"
        )
        done = _run(
            {"tool_name": "Bash", "tool_input": {"command": "echo hi"}},
            tmp,
        )
        done_body = _context(done)
        _assert("ACTIVE_BRANCH_NOTE" not in done_body, "done branch note was loaded")

        print("cursor journal hook tests passed")
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
