"""Cursor preToolUse journal hook loads the active branch only."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


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


def _fill_template(text: str, values: dict[str, str]) -> str:
    out = text
    for key, value in values.items():
        out = out.replace(f"**{key}:**", f"**{key}:** {value}")
    return out


def _run_hook(hook: Path, payload: dict, workspace: Path) -> str:
    completed = subprocess.run(
        [sys.executable, str(hook)],
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        cwd=str(workspace),
        check=False,
    )
    _assert(completed.returncode == 0, completed.stderr or "hook failed")
    return completed.stdout


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="cursor-journal-"))
    try:
        hook = ROOT / ".cursor" / "hooks" / "inject_journal_context.py"
        expert_tmpl = (ROOT / "journals" / "_TEMPLATE" / "expert" / "progress.md").read_text(
            encoding="utf-8"
        )
        wi_tmpl = (ROOT / "journals" / "work-items" / "_TEMPLATE" / "progress.md").read_text(
            encoding="utf-8"
        )
        node_tmpl = (
            ROOT / "journals" / "work-items" / "_TEMPLATE" / "nodes" / "work-item.md"
        ).read_text(encoding="utf-8")
        state_tmpl = (ROOT / "journals" / "work-items" / "_TEMPLATE" / "state.json").read_text(
            encoding="utf-8"
        )

        (tmp / ".cursor").mkdir(parents=True, exist_ok=True)
        expert = tmp / "journals" / "expert" / "progress.md"
        _write(
            expert,
            _fill_template(expert_tmpl, {"Current work item": "WID-1"}).replace(
                "**Premise and goal:** see the project spec and `MyRole.txt`",
                "EXPERT_JOURNAL\n\n**Premise and goal:** see the project spec and `MyRole.txt`",
            ),
        )
        base = tmp / "journals" / "work-items" / "WID-1"
        wi_body = wi_tmpl.replace("work-items/", "work-items/WID-1/")
        wi_body = wi_body.replace(
            "**Completion status:** not started",
            "**Completion status:** in progress",
        )
        _write(base / "progress.md", "WORK_ITEM_JOURNAL\n\n" + wi_body)
        state = json.loads(state_tmpl)
        state["active"] = ["work-item", "spec"]
        state.setdefault("nodes", {})
        state["nodes"]["work-item"] = {"parent": None, "status": "open", "history": []}
        state["nodes"]["spec"] = {"parent": "work-item", "status": "open", "history": []}
        state["nodes"]["implement"] = {
            "parent": "work-item",
            "status": "open",
            "history": [],
        }
        _write(base / "state.json", json.dumps(state))
        _write(base / "nodes" / "work-item.md", "ROOT_NOTE\n\n" + node_tmpl)
        _write(base / "nodes" / "spec.md", "ACTIVE_BRANCH_NOTE\n")
        _write(base / "nodes" / "implement.md", "INACTIVE_BRANCH_NOTE\n")

        # Case 1: active-context pointer
        (tmp / ".cursor" / "active-context.txt").write_text("work-item:WID-1\n", encoding="utf-8")
        body = _context(
            _run_hook(
                hook,
                {"tool_name": "Bash", "tool_input": {"command": "echo hi"}},
                tmp,
            )
        )
        _assert("EXPERT_JOURNAL" in body, "expert journal missing")
        _assert("WORK_ITEM_JOURNAL" in body, "work item journal missing")
        _assert("ACTIVE_BRANCH_NOTE" in body, "active branch missing")
        _assert("INACTIVE_BRANCH_NOTE" not in body, "inactive branch was loaded")

        # Case 2: no pointer files — work item from expert journal only
        (tmp / ".cursor" / "active-context.txt").unlink()
        from_expert_body = _context(
            _run_hook(
                hook,
                {"tool_name": "Bash", "tool_input": {"command": "echo hi"}},
                tmp,
            )
        )
        _assert("ACTIVE_BRANCH_NOTE" in from_expert_body, "expert-journal fallback failed")

        read_body = _context(
            _run_hook(
                hook,
                {
                    "tool_name": "Read",
                    "tool_input": {"file_path": "journals/work-items/WID-1/nodes/spec.md"},
                },
                tmp,
            )
        )
        _assert("ACTIVE_BRANCH_NOTE" not in read_body, "active note injected onto its own read")
        _assert("EXPERT_JOURNAL" in read_body, "expert journal dropped on note read")

        path_body = _context(
            _run_hook(
                hook,
                {
                    "tool_name": "Read",
                    "tool_input": {"path": "journals/work-items/WID-1/nodes/spec.md"},
                },
                tmp,
            )
        )
        _assert("ACTIVE_BRANCH_NOTE" not in path_body, "active note injected onto a path read")

        # Case 3: done status uses the template's bolded field
        done_text = (base / "progress.md").read_text(encoding="utf-8")
        done_text = done_text.replace(
            "**Completion status:** in progress",
            "**Completion status:** done",
        )
        (base / "progress.md").write_text(done_text, encoding="utf-8")
        done_body = _context(
            _run_hook(
                hook,
                {"tool_name": "Bash", "tool_input": {"command": "echo hi"}},
                tmp,
            )
        )
        _assert("ACTIVE_BRANCH_NOTE" not in done_body, "done branch note was loaded")
        _assert("WORK_ITEM_JOURNAL" in done_body, "done work item journal missing")
        print("cursor journal hook tests passed")
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
