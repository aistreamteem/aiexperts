# Background agent notes

Background agents write one markdown file here. The stop hook merges ready notes into the active leaf under `../nodes/`, then archives them in `merged/`.

## Loose notes

Put a single-agent note as `<label>.md` directly in this folder. It merges on the next Stop or SubagentStop.

## Shared tasks

For several agents sharing one task, use:

```text
tasks/<task-id>/
  manifest.json   { "task": "...", "subtasks": ["a", "b"], "deadline": "optional-iso" }
  a.md
  b.md
```

A shared task merges only when every subtask listed in the manifest has a note. A note whose `**Status:**` line contains `fail` marks the task partial. A task past its deadline escalates once via `NEEDS-ATTENTION.md`.

Do not write notes into `work-items/<id>/`. The real journal is under `journals/work-items/<id>/`.
