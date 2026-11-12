# Role workflows

Named jobs for the **Pest control office** role. Each file is a self-contained instruction for **continue** / **workflow-selector**. Do not skip a step with a chat summary. Data moves only as named files (`needs` / `produces`).

Jobs are listed in `workflow-registry.json`. Default workflow: `bait-map-index`. Typical daily start: `route-day` after `skip-list`. Method: `docs/role/work-item-method.md`.

## How to run

1. Open or confirm a Work Item under `work-items/<id>/`
2. **continue** walks one ready step (or the whole named job if requested)
3. **journal-keeper**

Initial phase for every job: `role-job`.

## Jobs

- [Bait Map Index](bait-map-index.md)
- [Callback List](callback-list.md)
- [Chemical Log Completeness](chemical-log-completeness.md)
- [Device Count](device-count.md)
- [Estimate From Price](estimate-from-price.md)
- [Inventory Chem Vs Log](inventory-chem-vs-log.md)
- [Route Day](route-day.md)
- [Skip List](skip-list.md)
- [Wdo Form Completeness](wdo-form-completeness.md)

## Work map shape

Human notes go under the YAML block in each job file.

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
| `needs` | Artifact ids that must already exist on disk under this Work Item. |
| `produces` | Artifact id this step writes. |
| `produce_path` | Path under `work/` (or `out/` for a finished pack), inside `work-items/<id>/`. |
| `tool` | File under `docs/tools/` to follow. |
| `check` | Command that exits **0** if the step passed, **non-zero** if not. Required. |
| `on_fail` | `retry` (at most 3) then **ask**. |
| `next` | Step ids that may run after this one passes. A next step still waits until its `needs` exist. |

## Rules

- Do not start a step if any `needs` file is missing.
- Do not start a step that has no `check` — propose a check (they must approve) or **ask**.
- Do not mark the job done until every step has a passing check.
- Rewrite `work/` and `out/` so they sit under the active Work Item folder.

## Memory

Role facts and rules: `facts/facts-operations.md` and `facts/rules-operations.md`.
