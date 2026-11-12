# Background-agent notes

Background agents write notes here. The stop hook merges them into the **active leaf** node under `../nodes/`, then archives processed files under `merged/`.

## Loose notes

Drop a single markdown file in this folder (not named `README.md`):

```text
journals/work-items/<id>/agent-notes/<label>.md
```

It is merged on the next stop / subagentStop.

## Shared tasks

For several agents on one task:

```text
journals/work-items/<id>/agent-notes/tasks/<task-id>/manifest.json
journals/work-items/<id>/agent-notes/tasks/<task-id>/<subtask>.md
```

`manifest.json` shape:

```json
{
  "task": "short name",
  "subtasks": ["a", "b"],
  "deadline": "2026-11-12T00:00:00Z"
}
```

The merge runs only when every listed subtask has a note. A note whose `Status:` line contains `fail` marks the task partial and writes `work-items/<id>/NEEDS-ATTENTION.md`. A task past its deadline with missing notes escalates once.
