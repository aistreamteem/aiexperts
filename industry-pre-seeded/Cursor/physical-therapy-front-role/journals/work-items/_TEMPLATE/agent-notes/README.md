# Agent notes

Background agents write loose notes or shared-task notes here. The stop hook merges them into the active leaf node under `../nodes/`.

## Loose note

Drop a single markdown file in this folder (not named `README.md`). Example:

```markdown
**Status:** done

What the background agent finished.
```

## Shared task

Create `tasks/<task-id>/manifest.json`:

```json
{
  "task": "short name",
  "subtasks": ["a", "b"],
  "deadline": "2026-11-11T23:59:59"
}
```

Each subtask agent writes `tasks/<task-id>/<subtask>.md`. Merge runs only when every listed subtask has a note. A note whose `**Status:**` line contains `fail` marks the task partial.

Processed notes move to `merged/`. Partial or stalled tasks also write `NEEDS-ATTENTION.md` on the Work Item artifact folder.
