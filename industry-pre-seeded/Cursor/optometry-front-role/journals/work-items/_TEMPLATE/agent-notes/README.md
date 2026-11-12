# Background-agent notes

Background agents write **here**, not into `progress.md` or the active node file.

## Loose notes

Drop one markdown file per agent under this folder:

```text
journals/work-items/<id>/agent-notes/<label>.md
```

Suggested fields:

```markdown
**Status:** succeeded | failed
**Summary:** one line

(Details the main session should fold into the journal.)
```

`README.md` itself is never merged.

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
  "deadline": "2026-11-11T23:59:59"
}
```

The merge hook waits until every listed subtask has a note (success or failure). Processed notes move to `merged/`.
