# Role workflows

Named jobs for the **Medical clinic front role (not the clinician)** role. Each file is a self-contained work map. **continue** walks one ready step. Data moves only as named files (`needs` / `produces`). Method: `docs/role/work-item-method.md`.

Jobs are listed in `workflow-registry.json`. Default workflow: `day-list`.

## How to run

1. Open or reuse `work-items/<id>/`. Put source files in `in/`.
2. Select the job (workflow-selector) if the journal has no Workflow type.
3. Follow this folder’s instruction file: read the named `docs/tools/` doc, write `produce_path` inside the Work Item, run the step `check`.
4. One ready step per continue unless the operator asked for the whole named job.
5. journal-keeper after each step.

Initial phase for every job: `role-job` (intake → map steps → `out/`).

## Jobs

- [Day List](day-list.md) (default)
- [Eligibility From Screenshot](eligibility-from-screenshot.md)
- [Intake Completeness](intake-completeness.md)
- [Wait List](wait-list.md)
- [Recall List If File](recall-list-if-file.md)
- [Referral Paperwork](referral-paperwork.md)
- [Records Release Log](records-release-log.md)
- [No Show List](no-show-list.md)
- [Day Close Tender](day-close-tender.md)

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
| `id` | Step name |
| `needs` | Artifact ids that must already exist on disk |
| `produces` | Artifact id this step writes |
| `produce_path` | Path under the Work Item `work/` or `out/` |
| `tool` | File under `docs/tools/` to follow |
| `check` | Command that exits **0** if the step passed |
| `on_fail` | `retry` (at most 3) then ask |
| `next` | Step ids that may run after this one passes |

## Rules

- Do not start a step if any `needs` file is missing.
- Do not start a step that has no `check` — propose a check and wait for approval, or ask.
- Do not mark the job done until every step has a passing check or a documented exception.
- Paths `work/` and `out/` mean inside `work-items/<id>/`.
