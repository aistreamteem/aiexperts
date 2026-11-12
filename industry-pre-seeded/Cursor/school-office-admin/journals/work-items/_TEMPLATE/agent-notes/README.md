# Background agent notes

Background agents write one markdown file here. The stop hook merges them into the active leaf under `../nodes/` and moves processed files into `merged/`.

## Loose notes

Create `<label>.md` in this folder. It is merged on the next stop / subagentStop.

Suggested fields:

```markdown
**Status:** ok
**Summary:** what the agent did

Notes...
```

Do not name a loose note `README.md`.

## Shared tasks

For several agents on one task, use:

```text
tasks/<task-id>/manifest.json
tasks/<task-id>/<subtask>.md
```

`manifest.json` example:

```json
{
  "task": "short description",
  "subtasks": ["a", "b"],
  "deadline": "2026-11-12T00:00:00Z"
}
```

The task merges only when every listed subtask has a note. A note whose `**Status:**` line contains `fail` marks the task partial. Past-deadline tasks with missing notes escalate once into `work-items/<id>/NEEDS-ATTENTION.md`.
