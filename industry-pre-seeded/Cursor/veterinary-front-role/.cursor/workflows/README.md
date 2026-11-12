# Role workflows

Named jobs for the **Veterinary front role (not the vet)** role. Each file is an expert workflow with a YAML work map. **continue** walks the map (one ready step unless the operator asked for the whole named job). Do not skip a step with a chat summary. Data moves only as named files (`needs` / `produces`).

Jobs are listed in `workflow-registry.json`. Default workflow: `day-appointments`.

## How to run

1. Open or reuse a Work Item under `work-items/<id>/`. Put source files in `in/`.
2. Select the registered job (workflow-selector if the journal has no Workflow type).
3. Follow this instruction file: one ready step per continue unless they asked for the whole named job.
4. Read the named `docs/tools/` doc. Write `produce_path` inside this Work Item. Run the step `check`.
5. **journal-keeper** after the step.

Initial phase for every job: `role-job`. Method: `docs/role/work-item-method.md`.

## Jobs

- [Day Appointments](day-appointments.md) (default)
- [Emergency Flag](emergency-flag.md)
- [New Client Forms](new-client-forms.md)
- [Records In](records-in.md)
- [Records Out](records-out.md)
- [Reminder List](reminder-list.md)
- [Estimate From Prices](estimate-from-prices.md)
- [Checkout List](checkout-list.md)
- [Board Dropoff](board-dropoff.md)

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
- Do not start a step that has no `check` — propose a check and wait for operator approval, or **ask**.
- Do not mark the job done until every step has a passing check.
