# Role workflows

Named jobs for the **Bookkeeping / bills** role. Each file is a self-contained instruction for **continue** / **workflow-selector**: when to use it, how to run it, and a YAML work map. Do not skip a step with a chat summary. Data moves only as named files (`needs` / `produces`) under the current Work Item.

Jobs are listed in `workflow-registry.json`. Default workflow: `month-end`.

Method: `docs/role/work-item-method.md`.

## How to run

1. Select the job (**workflow-selector**) and open `work-items/<id>/`
2. Put source files in `in/`
3. **continue** walks **one ready step** (or the whole named job if requested): read the tool doc, write the produced file, run the check, **journal-keeper**
4. On check fail, retry at most three times, then ask. If a step has no check, propose one and wait for approval

Initial phase for every job: first map step (usually gather / intake).

## Jobs

- [Month End](month-end.md)
- [Bank Review](bank-review.md)
- [Bank Reconcile](bank-reconcile.md)
- [Credit Card Code](credit-card-code.md)
- [Vendor Bills](vendor-bills.md)
- [Receipt Match](receipt-match.md)
- [AR Followup](ar-followup.md)
- [Sales Tax Questions](sales-tax-questions.md)
- [Contractor 1099 Year](contractor-1099-year.md)
- [Job Cost Light](job-cost-light.md)

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
    tool: docs/tools/some-tool.md
    check: python docs/tools/checks/file-exists.py out/done-file.md
    on_fail: retry
    next: []
```

| Field | Meaning |
| --- | --- |
| `id` | Step name (a part of the pack). |
| `needs` | Artifact ids that must already exist on disk in this Work Item. |
| `produces` | Artifact id this step writes. |
| `produce_path` | Path under this Work Item `work/` or `out/`. |
| `tool` | File under `docs/tools/` to follow. |
| `check` | Command that exits **0** if the step passed, **non-zero** if not. Required. |
| `on_fail` | `retry` (at most 3) then **ask**. |
| `next` | Step ids that may run after this one passes. A next step still waits until its `needs` exist. |

## Rules

- Do not start a step if any `needs` file is missing.
- Do not start a step that has no `check` — propose a check, get approval, then save it, or ask.
- Do not mark the job done until every step has a passing check.
- Paths `work/` and `out/` mean **inside** `work-items/<id>/`.
