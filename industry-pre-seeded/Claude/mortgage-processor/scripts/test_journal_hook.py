"""Cursor PreToolUse journal hook loads the active branch only."""

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


def _set_field(text: str, name: str, value: str) -> str:
    lines = []
    found = False
    for line in text.splitlines():
        if name.lower() in line.lower() and ":" in line:
            lines.append(f"**{name}:** {value}")
            found = True
        else:
            lines.append(line)
    if not found:
        lines.append(f"**{name}:** {value}")
    return "\n".join(lines) + "\n"


def _run(payload: dict, workspace: Path) -> str:
    completed = subprocess.run(
        [sys.executable, str(HOOK)],
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        cwd=str(workspace),
        check=False,
    )
    _assert(completed.returncode == 0, completed.stderr or completed.stdout or "hook failed")
    return _context(completed.stdout)


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="claude-journal-"))
    try:
        expert_tmpl = (ROOT / "journals" / "_TEMPLATE" / "expert" / "progress.md").read_text(
            encoding="utf-8"
        )
        wi_tmpl = (ROOT / "journals" / "work-items" / "_TEMPLATE" / "progress.md").read_text(
            encoding="utf-8"
        )
        node_tmpl = (
            ROOT / "journals" / "work-items" / "_TEMPLATE" / "nodes" / "work-item.md"
        ).read_text(encoding="utf-8")

        expert = tmp / "journals" / "expert" / "progress.md"
        _write(expert, "EXPERT_JOURNAL\n\n" + _set_field(expert_tmpl, "Current work item", "WID-1"))

        base = tmp / "journals" / "work-items" / "WID-1"
        progress = _set_field(wi_tmpl, "Completion status", "in progress")
        _write(base / "progress.md", "WORK_ITEM_JOURNAL\n\n" + progress)
        _write(
            base / "state.json",
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
        )
        _write(base / "nodes" / "work-item.md", "ROOT_NOTE\n" + node_tmpl)
        _write(base / "nodes" / "spec.md", "ACTIVE_BRANCH_NOTE\n")
        _write(base / "nodes" / "implement.md", "INACTIVE_BRANCH_NOTE\n")
        (tmp / ".claude").mkdir(parents=True, exist_ok=True)
        # No pointer files: work item resolved from expert journal only.

        body = _run(
            {"tool_name": "Bash", "tool_input": {"command": "echo hi"}},
            tmp,
        )
        _assert("EXPERT_JOURNAL" in body, "expert journal missing")
        _assert("WORK_ITEM_JOURNAL" in body, "work item journal missing")
        _assert("ACTIVE_BRANCH_NOTE" in body, "active branch missing")
        _assert("INACTIVE_BRANCH_NOTE" not in body, "inactive branch was loaded")

        read_body = _run(
            {
                "tool_name": "Read",
                "tool_input": {"file_path": "journals/work-items/WID-1/nodes/spec.md"},
            },
            tmp,
        )
        _assert("ACTIVE_BRANCH_NOTE" not in read_body, "active note injected onto its own read")
        _assert("EXPERT_JOURNAL" in read_body, "expert journal dropped on note read")

        path_body = _run(
            {
                "tool_name": "Read",
                "tool_input": {"path": "journals/work-items/WID-1/nodes/spec.md"},
            },
            tmp,
        )
        _assert("ACTIVE_BRANCH_NOTE" not in path_body, "active note injected onto a path read")

        done_text = _set_field(
            (base / "progress.md").read_text(encoding="utf-8"),
            "Completion status",
            "done",
        )
        (base / "progress.md").write_text(done_text, encoding="utf-8")
        done_body = _run(
            {"tool_name": "Bash", "tool_input": {"command": "echo hi"}},
            tmp,
        )
        _assert("ACTIVE_BRANCH_NOTE" not in done_body, "done branch note was loaded")
        _assert("WORK_ITEM_JOURNAL" in done_body, "done work item journal missing")
        print("claude journal hook tests passed")
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
