# agent-notes

Drop folder for background agents. Agents write here and never edit `progress.md` or node files directly. The Stop and SubagentStop hooks (`.claude/hooks/merge_agent_notes.py`) merge notes into the active leaf node, `../nodes/<leaf>.md`, and archive them under `merged/`.

## Loose note (single agent)

Write `agent-notes/<label>.md`. It is merged on the next hook run. This README is never merged.

## Shared task (several agents, one task)

Create `agent-notes/tasks/<task-id>/manifest.json`:

```json
{ "task": "short name", "subtasks": ["a", "b", "c"], "deadline": "2026-01-01T12:00:00-05:00" }
```

`deadline` is optional. Each subtask agent writes `agent-notes/tasks/<task-id>/<subtask>.md`, on success or when it gives up. A note whose `**Status:**` line contains "fail" marks the task partial and writes `work-items/<id>/NEEDS-ATTENTION.md`. The task merges only when every subtask has a note. Past the deadline with notes missing, the task is escalated once and `NEEDS-ATTENTION.md` is written.
