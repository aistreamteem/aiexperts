# Background agent notes

Background agents write one markdown file here. The stop hook merges ready notes into the **active leaf** under `../nodes/`, then moves processed files into `merged/`.

## Loose notes

Drop a single file such as `scale-check.md` directly in this folder (not in `tasks/`). It merges on the next stop hook.

Suggested fields:

```markdown
**Status:** ok
**Summary:** what finished

Notes...
```

Do not name a note `README.md` — that file is documentation only.

## Shared tasks

For several agents dividing one task, use:

```text
tasks/<task-id>/manifest.json
tasks/<task-id>/<subtask>.md
```

`manifest.json` example:

```json
{
  "task": "join receiving shorts",
  "subtasks": ["csv", "pdfs"],
  "deadline": "2026-11-12T18:00:00Z"
}
```

A shared task merges only when every listed subtask has a note. A note whose `Status` line contains `fail` marks the task partial. A task past its deadline with missing notes escalates once via `work-items/<id>/NEEDS-ATTENTION.md`.
