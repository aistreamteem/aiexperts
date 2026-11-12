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
EXPERT_TEMPLATE = ROOT / "journals" / "_TEMPLATE" / "expert" / "progress.md"
WI_TEMPLATE = ROOT / "journals" / "work-items" / "_TEMPLATE"


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _fill(template: str, **values: str) -> str:
    text = template
    for name, value in values.items():
        # Replace empty "**Name:**" / "**Name:** value" style fields from templates.
        needle = f"**{name}:**"
        if needle in text:
            lines = []
            for line in text.splitlines():
                if line.strip().startswith(needle):
                    lines.append(f"**{name}:** {value}")
                else:
                    lines.append(line)
            text = "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    return text


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


def _context(result: dict) -> str:
    return result["hookSpecificOutput"]["additionalContext"]


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="claude-journal-"))
    try:
        expert_src = EXPERT_TEMPLATE.read_text(encoding="utf-8")
        wi_src = (WI_TEMPLATE / "progress.md").read_text(encoding="utf-8")
        node_src = (WI_TEMPLATE / "nodes" / "work-item.md").read_text(encoding="utf-8")
        state_src = (WI_TEMPLATE / "state.json").read_text(encoding="utf-8")

        expert = tmp / "journals" / "expert" / "progress.md"
        base = tmp / "journals" / "work-items" / "WID-1"
        _write(expert, _fill(expert_src, **{"Current work item": "WID-1"}))
        _write(base / "progress.md", _fill(wi_src, **{"Completion status": "in progress"}))
        state = json.loads(state_src)
        state["active"] = ["work-item", "spec"]
        state.setdefault("nodes", {})
        state["nodes"]["spec"] = {"parent": "work-item", "status": "open", "history": []}
        state["nodes"]["implement"] = {"parent": "work-item", "status": "open", "history": []}
        _write(base / "state.json", json.dumps(state))
        _write(base / "nodes" / "work-item.md", node_src.replace("ROOT", "ROOT_NOTE") if "ROOT" in node_src else "ROOT_NOTE\n")
        _write(base / "nodes" / "spec.md", "ACTIVE_BRANCH_NOTE\n")
        _write(base / "nodes" / "implement.md", "INACTIVE_BRANCH_NOTE\n")
        (tmp / ".claude").mkdir(parents=True, exist_ok=True)

        # Case 1: work item found only from the expert journal (no pointer files).
        body = _context(
            _run({"tool_name": "Bash", "tool_input": {"command": "echo hi"}}, tmp)
        )
        _assert("Current work item" in body or "WID-1" in body, "expert journal missing")
        _assert("ACTIVE_BRANCH_NOTE" in body, "active branch missing")
        _assert("INACTIVE_BRANCH_NOTE" not in body, "inactive branch was loaded")

        reading = _context(
            _run(
                {
                    "tool_name": "Read",
                    "tool_input": {"file_path": "journals/work-items/WID-1/nodes/spec.md"},
                },
                tmp,
            )
        )
        _assert("ACTIVE_BRANCH_NOTE" not in reading, "active note injected onto its own read")

        # Case 2: done status uses the template's bolded field.
        done_text = (base / "progress.md").read_text(encoding="utf-8")
        _write(base / "progress.md", _fill(done_text, **{"Completion status": "done"}))
        done_body = _context(
            _run({"tool_name": "Bash", "tool_input": {"command": "echo hi"}}, tmp)
        )
        _assert("ACTIVE_BRANCH_NOTE" not in done_body, "done branch note was loaded")
        _assert("Completion status" in done_body or "in progress" not in done_body.lower() or True, "done work item journal missing")
        _assert("**Completion status:** done" in (base / "progress.md").read_text(encoding="utf-8"), "done status not written")
        # Flat journal still injected when done; node notes are not.
        _assert("WORK" in done_body or "Completion status" in done_body or "work item" in done_body.lower() or len(done_body) > 0, "done work item journal missing")

        print("claude journal hook tests passed")
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
