# Role workflows

Named jobs for **Optometry front role (not the doctor)**. Each job is registered in `workflow-registry.json` and has an instruction file in this folder. **continue** walks one ready YAML step (or the whole named job if requested). Do not skip a step with a chat summary. Data moves only as named files (`needs` / `produces`).

Default job: **day-list**. Method: `docs/role/work-item-method.md`.

## Available jobs

| Job | Instruction file |
| --- | --- |
| Day List | `.cursor/workflows/day-list.md` |
| Eligibility Screenshot | `.cursor/workflows/eligibility-screenshot.md` |
| Wait List | `.cursor/workflows/wait-list.md` |
| Frame Lens Order Completeness | `.cursor/workflows/frame-lens-order-completeness.md` |
| Missing Rx On Order | `.cursor/workflows/missing-rx-on-order.md` |
| Pickup Notify List | `.cursor/workflows/pickup-notify-list.md` |
| Recall List | `.cursor/workflows/recall-list.md` |
| Redo Log | `.cursor/workflows/redo-log.md` |
| Day Close | `.cursor/workflows/day-close.md` |

## How to run

1. Open or reuse one folder under `work-items/<id>/` per appointment, ticket, period, or pack
2. Walk one ready map step (or the whole named job if requested)
3. **journal-keeper**

**Initial phase:** `intake`, then the first YAML step. Paths `work/` and `out/` mean inside the current Work Item.

Role memory: `facts/facts-operations.md` and `facts/rules-operations.md`. Tools live under `docs/tools/`.

## Work map (required shape)

YAML lives in the job instruction file. Human notes go under it.

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
    produce_path: work/done-file.csv
    tool: docs/tools/some-tool.md
    check: python docs/tools/checks/file-exists.py work/done-file.csv
    on_fail: retry
    next: []
```

| Field | Meaning |
| --- | --- |
| `id` | Step name. |
| `needs` | Artifact ids that must already exist on disk in this Work Item. |
| `produces` | Artifact id this step writes. |
| `produce_path` | Path under `work/` (or `out/` for a finished pack), inside the Work Item. |
| `tool` | File under `docs/tools/` to follow. |
| `check` | Command that exits **0** if the step passed, **non-zero** if not. Required. |
| `on_fail` | `retry` (at most 3) then **ask**. |
| `next` | Step ids that may run after this one passes. A next step still waits until its `needs` exist. |

## Rules

- Do not start a step if any `needs` file is missing.
- Do not start a step that has no `check` — propose a check and wait for operator approval, or **ask**.
- Do not mark the job done until every step has a passing check.

## Adding a job

1. Add `.cursor/workflows/<id>.md` with When to use, How to run, Initial phase, and a YAML work map.
2. Register it in `workflow-registry.json` (job id = filename stem).
3. Point `MyRole.txt` and `AGENTS.md` at the new path. Update `docs/role/work-item-method.md`.
