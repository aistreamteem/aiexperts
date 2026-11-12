# Role workflows

Named jobs for the **Equipment rental role**. Each file is a self-contained instruction for **continue** / **workflow-selector**. Follow the YAML steps. Do not skip a step with a chat summary. Data moves only as named files (`needs` / `produces`).

Jobs are listed in `workflow-registry.json`. Default workflow: `contract-completeness`.

Work Item method: `docs/role/work-item-method.md`.

## How to run

1. Open or continue a Work Item under `work-items/<id>/` (**workflow-selector** if the job is not chosen).
2. Follow **this job file** one ready step (or the whole named job if requested).
3. Read the named file under `docs/tools/`. Write `produce_path` inside the Work Item (`work/` and `out/` mean `work-items/<id>/work/` and `work-items/<id>/out/`).
4. Run the step’s check against those paths. Retry a failed check at most 3 times, then ask.
5. **journal-keeper**.

Initial phase for every job: first step in that file’s YAML.

## Jobs

- [Contract Completeness](contract-completeness.md)
- [Delivery Tickets](delivery-tickets.md)
- [Maintenance Due](maintenance-due.md)
- [Meter Exceptions](meter-exceptions.md)
- [Outgoing Inspection](outgoing-inspection.md)
- [Renter COI Missing](renter-coi-missing.md)
- [Reservation Day](reservation-day.md)
- [Return Damage](return-damage.md)
- [Utilization](utilization.md)

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
    produce_path: out/done-file.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/done-file.md
    on_fail: retry
    next: []
```

| Field | Meaning |
| --- | --- |
| `id` | Step name. |
| `needs` | Artifact ids that must already exist on disk in this Work Item. |
| `produces` | Artifact id this step writes. |
| `produce_path` | Path under this Work Item’s `work/` (or `out/` for a finished pack). |
| `tool` | File under `docs/tools/` to follow. |
| `check` | Command that exits **0** if the step passed, **non-zero** if not. Required. |
| `on_fail` | `retry` (at most 3) then **ask**. |
| `next` | Step ids that may run after this one passes. A next step still waits until its `needs` exist. |

## Rules

- Do not start a step if any `needs` file is missing.
- Do not start a step that has no `check` — propose a check and get approval, or **ask**.
- Do not mark the job done until every step has a passing check or a documented exception.
- Do not invent rates, meters, serials, zones, deposits, or fees. Ask.
