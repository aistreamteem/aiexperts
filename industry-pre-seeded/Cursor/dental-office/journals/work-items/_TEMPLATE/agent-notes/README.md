# Background agent notes

Drop one markdown file per background agent here. The stop hook merges ready notes into the active leaf under `../nodes/`.

## Loose notes

- Create `journals/work-items/<id>/agent-notes/<label>.md`
- Merged on the next stop / subagentStop
- Processed files move to `merged/`

## Shared tasks

- Folder: `tasks/<task-id>/`
- `manifest.json`:

```json
{
  "task": "short description",
  "subtasks": ["a", "b"],
  "deadline": "2026-11-12T18:00:00Z"
}
```

- Each subtask writes `<name>.md` when it finishes (success or give-up)
- A `**Status:** failed` line marks that subtask failed
- Merge happens only when every listed subtask has a note
