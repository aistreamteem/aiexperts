# Background-agent notes

Drop loose notes here as `*.md` (not this README). The stop hook merges them into the active leaf node under `../nodes/`, then moves them to `merged/`.

## Loose note

```markdown
**Status:** ok
**Summary:** one line

Body of findings...
```

## Shared task

Create `tasks/<task-id>/manifest.json` with a `subtasks` list and optional `deadline`. Each subtask writes `tasks/<task-id>/<name>.md`. Merge runs only when every named subtask file is present.
