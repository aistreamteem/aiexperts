# Role workflows

Named jobs for the **Moving company office** role. Each file is a self-contained instruction with a YAML work map. **continue** walks one ready step. Do not skip a step with a chat summary. Data moves only as named files (`needs` / `produces`). Paths `work/` and `out/` are inside `work-items/<id>/`.

Jobs are listed in `workflow-registry.json`. Default workflow: `estimate-from-rate-file`. Role method: `docs/role/work-item-method.md`.

## How to run

1. **workflow-selector** if the Work Item has no workflow type
2. Follow this job’s instruction file (tool doc → produce artifact → run check)
3. **journal-keeper**

Initial phase for every job: `role-job` (see the method note for intake / inventory / estimate / dispatch / load-docs / claims).

## Jobs

- [Estimate From Rate File](estimate-from-rate-file.md)
- [Inventory Completeness](inventory-completeness.md)
- [High Value List Check](high-value-list-check.md)
- [Materials List](materials-list.md)
- [Crew Day](crew-day.md)
- [Truck Calendar](truck-calendar.md)
- [Delivery Window List](delivery-window-list.md)
- [Weigh Ticket Pack](weigh-ticket-pack.md)
- [Claims Routing](claims-routing.md)

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
```

| Field | Meaning |
| --- | --- |
| `id` | Step name. |
| `needs` | Artifact ids that must already exist on disk. |
| `produces` | Artifact id this step writes. |
| `produce_path` | Path under the Work Item `work/` (or `out/` for a finished pack). |
| `tool` | File under `docs/tools/` to follow. |
| `check` | Command that exits **0** if the step passed, **non-zero** if not. Required. |
| `on_fail` | `retry` (at most 3) then **ask**. |
| `next` | Step ids that may run after this one passes. |

## Rules

- Do not start a step if any `needs` file is missing.
- Do not start a step that has no `check` — ask the operator.
- Do not mark the job done until every step has a passing check.
