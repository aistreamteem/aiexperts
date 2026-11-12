# Background-agent notes

Pending notes from background agents live here. The stop hook merges them into the active leaf node under `journals/work-items/<id>/nodes/`, then moves processed files into `merged/`.

## Loose notes

Drop a single markdown file in this folder (not in `tasks/`):

```markdown
**Status:** ok

Notes from the background agent…
```

Do not name a loose note `README.md`.

## Shared tasks

For work split across subagents, use:

```
tasks/<task-id>/manifest.json
tasks/<task-id>/<subtask>.md
```

`manifest.json` example:

```json
{
  "task": "short title",
  "session_dir": "work-items/<id>",
  "subtasks": ["a", "b"],
  "deadline": "2026-11-12T00:00:00"
}
```

Each subtask writes `<subtask>.md` on success or give-up. A `**Status:**` line containing `fail` marks that subtask failed. The merge waits until every listed subtask has a note (or escalates once past `deadline`).
