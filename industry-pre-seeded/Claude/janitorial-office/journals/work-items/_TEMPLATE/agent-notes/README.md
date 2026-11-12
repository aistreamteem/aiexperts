# Background agent notes

Drop loose notes as `*.md` files in this folder. Shared tasks go under `tasks/<task-id>/` with a `manifest.json` listing subtasks.

The stop hook merges notes into the active leaf under `../nodes/` via `merge_agent_notes.py`, then archives processed files under `merged/`.

## Loose note format

```markdown
**Status:** ok | failed
**Summary:** one line

Notes body…
```

## Shared task

`manifest.json`:

```json
{ "task": "name", "deadline": "2026-01-01T00:00:00Z", "subtasks": ["a", "b"] }
```

Each subtask writes `<name>.md` in the task folder using the same note format.
