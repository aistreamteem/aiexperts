"""Claude PreToolUse journal hook loads the active branch only."""

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


def _run(payload: dict, workspace: Path) -> str:
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
    return completed.stdout


def _fill_templates(tmp: Path) -> Path:
    """Copy real journal templates and fill values the hook must read."""
    shutil.copytree(ROOT / "journals" / "_TEMPLATE" / "expert", tmp / "journals" / "expert")
    wi_src = ROOT / "journals" / "work-items" / "_TEMPLATE"
    base = tmp / "journals" / "work-items" / "WID-1"
    shutil.copytree(wi_src, base)

    expert = tmp / "journals" / "expert" / "progress.md"
    expert_text = expert.read_text(encoding="utf-8")
    expert_text = expert_text.replace("**Current work item:**", "**Current work item:** WID-1")
    expert.write_text("EXPERT_JOURNAL\n\n" + expert_text, encoding="utf-8")

    flat = base / "progress.md"
    flat_text = flat.read_text(encoding="utf-8")
    flat_text = flat_text.replace(
        "**Completion status:** not started",
        "**Completion status:** in progress",
    )
    flat.write_text("WORK_ITEM_JOURNAL\n\n" + flat_text, encoding="utf-8")

    state = {
        "active": ["work-item", "spec"],
        "nodes": {
            "work-item": {"parent": None, "status": "open", "history": []},
            "spec": {"parent": "work-item", "status": "open", "history": []},
            "implement": {"parent": "work-item", "status": "open", "history": []},
        },
    }
    (base / "state.json").write_text(json.dumps(state), encoding="utf-8")
    _write(base / "nodes" / "work-item.md", "ROOT_NOTE\n\n**Next action:**\n")
    _write(base / "nodes" / "spec.md", "ACTIVE_BRANCH_NOTE\n\n**Next action:** continue\n")
    _write(base / "nodes" / "implement.md", "INACTIVE_BRANCH_NOTE\n")
    (tmp / ".claude").mkdir(parents=True, exist_ok=True)
    return base


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="claude-journal-"))
    try:
        base = _fill_templates(tmp)
        (tmp / ".claude" / "active-context.txt").write_text(
            "work-item:WID-1\n", encoding="utf-8"
        )

        body = _context(
            _run({"tool_name": "Bash", "tool_input": {"command": "echo hi"}}, tmp)
        )
        _assert("EXPERT_JOURNAL" in body, "expert journal missing")
        _assert("WORK_ITEM_JOURNAL" in body, "work item journal missing")
        _assert("ACTIVE_BRANCH_NOTE" in body, "active branch missing")
        _assert("INACTIVE_BRANCH_NOTE" not in body, "inactive branch was loaded")

        # No pointer files: work item found only from expert journal line
        (tmp / ".claude" / "active-context.txt").unlink(missing_ok=True)
        body2 = _context(
            _run({"tool_name": "Bash", "tool_input": {"command": "echo hi"}}, tmp)
        )
        _assert("ACTIVE_BRANCH_NOTE" in body2, "fallback from expert journal failed")

        (tmp / ".claude" / "active-context.txt").write_text(
            "work-item:WID-1\n", encoding="utf-8"
        )

        read_body = _context(
            _run(
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
        _assert("EXPERT_JOURNAL" in read_body, "expert journal dropped on note read")

        path_body = _context(
            _run(
                {
                    "tool_name": "Read",
                    "tool_input": {"path": "journals/work-items/WID-1/nodes/spec.md"},
                },
                tmp,
            )
        )
        _assert(
            "ACTIVE_BRANCH_NOTE" not in path_body,
            "active note injected onto a path read",
        )

        flat = base / "progress.md"
        flat.write_text(
            flat.read_text(encoding="utf-8").replace(
                "**Completion status:** in progress",
                "**Completion status:** done",
            ),
            encoding="utf-8",
        )
        done_body = _context(
            _run({"tool_name": "Bash", "tool_input": {"command": "echo hi"}}, tmp)
        )
        _assert("ACTIVE_BRANCH_NOTE" not in done_body, "done branch note was loaded")
        _assert("WORK_ITEM_JOURNAL" in done_body, "done work item journal missing")
        print("claude journal hook tests passed")
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
