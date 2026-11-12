# Role workflows

Named jobs for the **Construction office coordinator**. Each job is a registry entry in `workflow-registry.json` with an instruction file in this folder. **continue** walks one ready step. Do not skip a step with a chat summary. Data moves only as named files (`needs` / `produces`) inside `work-items/<id>/`.

Default workflow: `daily-log`. Method: `docs/role/work-item-method.md`.

## Jobs

| Id | Name | Instruction file |
| --- | --- | --- |
| change-register | Change Register | `.cursor/workflows/change-register.md` |
| closeout-binder | Closeout Binder | `.cursor/workflows/closeout-binder.md` |
| daily-log | Daily Log | `.cursor/workflows/daily-log.md` |
| deliveries | Deliveries | `.cursor/workflows/deliveries.md` |
| look-ahead | Look Ahead | `.cursor/workflows/look-ahead.md` |
| punch-list | Punch List | `.cursor/workflows/punch-list.md` |
| rfi-status | RFI Status | `.cursor/workflows/rfi-status.md` |
| sub-coi | Sub COI | `.cursor/workflows/sub-coi.md` |
| submittal-aging | Submittal Aging | `.cursor/workflows/submittal-aging.md` |
| weekly-minutes | Weekly Minutes | `.cursor/workflows/weekly-minutes.md` |

## How to run

1. Select or create a Work Item under `work-items/<id>/` (use **workflow-selector** if the journal has no workflow type)
2. Follow the instruction file: intake → extract → exception pass (if any) → pack
3. **journal-keeper** after each step

Every role job starts in phase `intake`.

## Work map (required shape)

Put this YAML block in `.cursor/workflows/<name>.md`. Human notes go under it. Paths are relative to the current Work Item folder.

```yaml
id: job-name
steps:
  - id: first-step
    needs: []
    produces: artifact-id
    produce_path: work/artifact-id.csv
    tool: docs/tools/some-tool.md
    check: python docs/tools/checks/file-exists.py work/artifact-id.csv
    on_fail: retry
    next: [second-step]
  - id: second-step
    needs: [artifact-id]
    produces: done-file
    produce_path: out/done-file.md
    tool: docs/tools/some-tool.md
    check: python docs/tools/checks/file-exists.py out/done-file.md
    on_fail: retry
    next: []
```

| Field | Meaning |
| --- | --- |
| `id` | Step name |
| `needs` | Artifact ids that must already exist on disk |
| `produces` | Artifact id this step writes |
| `produce_path` | Path under `work/` or `out/` inside the Work Item |
| `tool` | File under `docs/tools/` to follow |
| `check` | Command that exits **0** if the step passed |
| `on_fail` | `retry` (at most 3) then ask |
| `next` | Step ids that may run after this one passes |

## Rules

- Do not start a step if any `needs` file is missing.
- Do not start a step that has no check — ask what would prove it, save a check only after they approve.
- Do not mark the job done until every step has a passing check or a recorded exception.

## Adding a job

1. Add `.cursor/workflows/<id>.md` with **When to use**, **How to run**, **Initial phase** `intake`, and a YAML work map.
2. Register `<id>` in `workflow-registry.json`.
3. Point `MyRole.txt`, `AGENTS.md`, and `docs/role/work-item-method.md` at the new file.
