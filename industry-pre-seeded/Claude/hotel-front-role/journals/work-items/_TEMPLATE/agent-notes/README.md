# Background agent notes

Background agents write notes here. The stop hook merges them into the **active leaf** node under `../nodes/`, then archives processed files in `merged/`.

## Loose note

Drop a single markdown file (not named `README.md`) in this folder:

```markdown
**Status:** ok

What the agent did…
```

## Shared task

Create `tasks/<task-id>/manifest.json`:

```json
{
  "task": "short description",
  "subtasks": ["a", "b"],
  "deadline": "2026-11-12T00:00:00Z"
}
```

Each subtask agent writes `tasks/<task-id>/<subtask>.md`. The merge runs only when every listed subtask has a note. A note whose **Status** contains `fail` marks the task partial and writes `work-items/<id>/NEEDS-ATTENTION.md`.
