# Role workflows

Named jobs for the **Landscaping / lawn-care office** role. Each file is a self-contained instruction for **continue**: steps with `needs` / `produces` / a check. Do not skip a step with a chat summary. Data moves only as named files. Method: `docs/role/work-item-method.md`.

Jobs are listed in `workflow-registry.json`. Default workflow: `callback-list`. Typical daily dispatch: `crew-day`.

## How to run

1. Open or continue a Work Item under `work-items/<id>/` (**workflow-selector** if Workflow type is missing)
2. **continue** walks one ready step from the selected file (or the whole named job if requested)
3. **journal-keeper**

Paths `work/` and `out/` in a map mean **inside that Work Item folder**.

Initial phase for every job: `role-job` (first ready step in the file).

## Jobs

- [Callback List](callback-list.md)
- [Crew Day](crew-day.md)
- [Enhancement Ticket](enhancement-ticket.md)
- [Estimate From Price](estimate-from-price.md)
- [Material Pull](material-pull.md)
- [Photo Pack](photo-pack.md)
- [Route Pack](route-pack.md)
- [Seasonal Calendar](seasonal-calendar.md)
- [Weather Postpone List](weather-postpone-list.md)

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
| `id` | Step name |
| `needs` | Artifact ids that must already exist on disk in this Work Item |
| `produces` | Artifact id this step writes |
| `produce_path` | Path under this Work Item’s `work/` (or `out/` for a finished pack) |
| `tool` | File under `docs/tools/` to follow |
| `check` | Command that exits **0** if the step passed, **non-zero** if not. Required |
| `on_fail` | `retry` (at most 3) then **ask** |
| `next` | Step ids that may run after this one passes |

## Rules

- Do not start a step if any `needs` file is missing.
- Do not start a step that has no `check` — ask the operator how they will know it is done.
- Do not mark the job done until every step has a passing check or a documented exception.
- Do not invent a ticket, price, weather call, mix, or wage.
