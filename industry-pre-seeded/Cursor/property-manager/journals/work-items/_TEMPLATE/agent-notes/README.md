# Background agent notes

Background agents write notes here. The stop / subagentStop hooks merge them into the active leaf node under `journals/work-items/<id>/nodes/`.

## Loose notes

Drop a single markdown file in this folder (not `README.md`):

```text
journals/work-items/<id>/agent-notes/<label>.md
```

It is merged on the next stop hook and moved to `merged/`.

## Shared tasks

When several agents split one task:

```text
journals/work-items/<id>/agent-notes/tasks/<task-id>/manifest.json
journals/work-items/<id>/agent-notes/tasks/<task-id>/<subtask>.md
```

`manifest.json` example:

```json
{
  "task": "Index application PDFs",
  "subtasks": ["a", "b"],
  "deadline": "2026-11-12T18:00:00+00:00"
}
```

The task merges only when every listed subtask has a note file. A note whose **Status:** line contains `fail` marks the task partial. Past-deadline tasks with missing notes escalate once into `work-items/<id>/NEEDS-ATTENTION.md`.

Do not write step notes under the Work Item artifact tree; use `nodes/` via journal-keeper.
