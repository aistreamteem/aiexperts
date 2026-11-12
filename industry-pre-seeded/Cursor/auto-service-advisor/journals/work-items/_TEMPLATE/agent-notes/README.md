# Background agent notes

Background agents write notes here. The stop hook merges them into the **active leaf** node under `../nodes/`, then moves processed files into `merged/`.

## Loose note (one agent)

Create `journals/work-items/<id>/agent-notes/<label>.md`:

```markdown
**Status:** ok

What the agent did, findings, and any open questions.
```

Merged on the next stop / subagentStop.

## Shared task (several subtasks)

Create `journals/work-items/<id>/agent-notes/tasks/<task-id>/`:

- `manifest.json` — `{ "task": "...", "subtasks": ["a", "b"], "deadline": "<optional ISO8601>" }`
- One `<subtask>.md` per subtask when that agent finishes (success or give-up).

A shared task merges only when every listed subtask has a note. A note whose Status line contains `fail` marks the task partial and writes `work-items/<id>/NEEDS-ATTENTION.md`.

Do not edit `README.md` as a note; it is ignored by the merger.
