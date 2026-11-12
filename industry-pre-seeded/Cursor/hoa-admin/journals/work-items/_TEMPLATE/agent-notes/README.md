# Background-agent notes

Drop loose notes as `*.md` files in this folder (not `README.md`). Shared multi-agent tasks go under `tasks/<task-id>/` with a `manifest.json` and one `<subtask>.md` per agent.

The stop / subagentStop hooks merge ready notes into the active leaf under `../nodes/`, then archive sources under `merged/`.

## Loose note

```markdown
**Status:** complete

Notes for journal-keeper to fold into the right sections.
```

## Shared task

`tasks/<task-id>/manifest.json`:

```json
{
  "task": "short label",
  "subtasks": ["a", "b"],
  "deadline": "2026-11-12T18:00:00"
}
```

Each subtask writes `tasks/<task-id>/<name>.md`. A `**Status:**` line containing `fail` marks that subtask failed. The task merges only when every listed subtask file exists.
