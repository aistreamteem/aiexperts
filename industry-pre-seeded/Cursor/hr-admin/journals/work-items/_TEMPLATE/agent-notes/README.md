# Background-agent notes

Drop one markdown file per background agent here. The stop / subagentStop hook merges them into the active leaf under `nodes/`, then moves processed files into `merged/`.

## Loose notes

`journals/work-items/<id>/agent-notes/<label>.md`

Merged on the next stop hook fire.

## Shared tasks

`journals/work-items/<id>/agent-notes/tasks/<task-id>/`

- `manifest.json` with `task`, optional `deadline`, and `subtasks: ["a","b"]`
- One `<subtask>.md` per agent (success or failure). A `Status:` line containing `fail` marks that subtask failed.
- Merge runs only when every subtask file is present. Partial / stalled tasks write `work-items/<id>/NEEDS-ATTENTION.md`.

Do not write notes into `progress.md` from background agents — the merge hook owns that.
