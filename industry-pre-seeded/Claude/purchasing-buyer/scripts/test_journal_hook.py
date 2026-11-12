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


def _run(payload: dict, workspace: Path) -> str:
    completed = subprocess.run(
        [sys.executable, str(HOOK)],
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        cwd=str(workspace),
        check=False,
    )
    _assert(completed.returncode == 0, completed.stderr or "hook failed")
    return completed.stdout


def _set_completion(progress: str, status: str) -> str:
    lines = []
    found = False
    for line in progress.splitlines():
        if "Completion status" in line and ":" in line:
            lines.append(f"**Completion status:** {status}")
            found = True
        else:
            lines.append(line)
    if not found:
        lines.append(f"**Completion status:** {status}")
    return "\n".join(lines) + "\n"


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="claude-journal-"))
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
        expert_text = expert_tmpl
        if "**Current work item:**" in expert_text:
            expert_text = expert_text.replace(
                "**Current work item:**", "**Current work item:** WID-1", 1
            )
        else:
            expert_text = expert_text.rstrip() + "\n\n**Current work item:** WID-1\n"
        _write(tmp / "journals" / "expert" / "progress.md", expert_text)

        base = tmp / "journals" / "work-items" / "WID-1"
        flat = wi_tmpl.replace("work-items/", "work-items/WID-1/", 1)
        flat = _set_completion(flat, "in progress")
        _write(base / "progress.md", flat)

        try:
            state = json.loads(state_tmpl)
        except json.JSONDecodeError:
            state = {}
        if not isinstance(state, dict):
            state = {}
        state["active"] = ["work-item", "spec"]
        nodes = state.setdefault("nodes", {})
        if isinstance(nodes, dict):
            nodes.setdefault("work-item", {"parent": None, "status": "open", "history": []})
            nodes.setdefault("spec", {"parent": "work-item", "status": "open", "history": []})
            nodes.setdefault("implement", {"parent": "work-item", "status": "open", "history": []})
        _write(base / "state.json", json.dumps(state))
        _write(base / "nodes" / "work-item.md", node_tmpl if node_tmpl.strip() else "ROOT_NOTE\n")
        _write(base / "nodes" / "spec.md", "ACTIVE_BRANCH_NOTE\n")
        _write(base / "nodes" / "implement.md", "INACTIVE_BRANCH_NOTE\n")

        (tmp / ".claude" / "active-context.txt").write_text("work-item:WID-1\n", encoding="utf-8")
        body = _context(_run({"tool_name": "Bash", "tool_input": {"command": "echo hi"}}, tmp))
        _assert("ACTIVE_BRANCH_NOTE" in body, "active branch missing")
        _assert("INACTIVE_BRANCH_NOTE" not in body, "inactive branch was loaded")

        (tmp / ".claude" / "active-context.txt").unlink(missing_ok=True)
        legacy = tmp / ".claude" / "active-work-item.txt"
        if legacy.is_file():
            legacy.unlink()
        from_body = _context(
            _run({"tool_name": "Bash", "tool_input": {"command": "echo hi"}}, tmp)
        )
        _assert("ACTIVE_BRANCH_NOTE" in from_body, "journal fallback missed active branch")

        read_body = _context(
            _run(
                {
                    "tool_name": "Read",
                    "tool_input": {"file_path": "journals/work-items/WID-1/nodes/spec.md"},
                },
                tmp,
            )
        )
        _assert("ACTIVE_BRANCH_NOTE" not in read_body, "active note injected onto its own read")

        (base / "progress.md").write_text(
            _set_completion((base / "progress.md").read_text(encoding="utf-8"), "done"),
            encoding="utf-8",
        )
        (tmp / ".claude" / "active-context.txt").write_text("work-item:WID-1\n", encoding="utf-8")
        done_body = _context(
            _run({"tool_name": "Bash", "tool_input": {"command": "echo hi"}}, tmp)
        )
        _assert("ACTIVE_BRANCH_NOTE" not in done_body, "done branch note was loaded")
        print("claude journal hook tests passed")
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
