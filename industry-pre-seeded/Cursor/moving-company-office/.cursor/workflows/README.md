# Role workflows

Named jobs for the **Moving company office** role. Each file is a self-contained work map for **continue** / **workflow-selector**. Data moves only as named files (`needs` / `produces`). Paths `in/`, `work/`, `out/`, and `evidence/` are inside `work-items/<id>/`.

Jobs are listed in `workflow-registry.json`. Default workflow: `estimate-from-rate-file`. Method: `docs/role/work-item-method.md`.

## How to run

1. Open or continue a Work Item under `work-items/<id>/`. Put source files in that item’s `in/`.
2. Read the matching job file below and the named `docs/tools/` doc.
3. Walk **one ready YAML step** (or the whole named job if requested): produce the file, run the check, then **journal-keeper**.
4. Do not skip a step with a chat summary. If a `needs` file is missing, ask. Retry a failed check at most 3 times, then ask.

Initial phase for every job: isolate the Work Item, then walk the map.

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
| `id` | Step name (a part of the job). |
| `needs` | Artifact ids that must already exist on disk in this Work Item. |
| `produces` | Artifact id this step writes. |
| `produce_path` | Path under this Work Item’s `work/` (or `out/` for a finished pack). |
| `tool` | File under `docs/tools/` to follow. |
| `check` | Command that exits **0** if the step passed. Required. Run it so paths resolve inside this Work Item. |
| `on_fail` | `retry` (at most 3) then **ask**. |
| `next` | Step ids that may run after this one passes. A next step still waits until its `needs` exist. |

## Rules

- Do not start a step if any `needs` file is missing.
- Do not start a step that has no check — propose a check and wait for approval, or ask.
- Do not mark the job done until every step has a passing check (or a documented exception in the journal).
