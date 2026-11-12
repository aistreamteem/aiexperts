# Background agent notes

Background agents write here. The stop hook merges ready notes into the active leaf under `nodes/`, then archives them in `merged/`.

## Loose note

Create one markdown file per agent in this folder (not under `tasks/`):

```markdown
**Status:** ok
**Summary:** what this agent did

Details...
```

`README.md` is ignored by the merger.

## Shared task

Create `tasks/<task-id>/manifest.json`:

```json
{
  "task": "short name",
  "subtasks": ["a", "b"],
  "deadline": "2026-11-12T00:00:00Z"
}
```

Each subtask agent writes `tasks/<task-id>/<subtask>.md`. The merger waits until every listed subtask has a note. A note whose `**Status:**` contains `fail` marks the task partial and writes `work-items/<id>/NEEDS-ATTENTION.md`.
