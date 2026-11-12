# Role workflows

Named jobs for the **Medical clinic front role (not the clinician)** role. Each file is a self-contained instruction for **continue** / **workflow-selector**. Follow the steps in the file. Do not skip a step with a chat summary. Data moves only as named files (`needs` / `produces`).

Jobs are listed in `workflow-registry.json`. Default workflow: `day-list`. Method: `docs/role/work-item-method.md`.

## How to run

1. Open or continue a Work Item under `work-items/<id>/` (copy `_TEMPLATE` if needed). Put source files in `in/`.
2. Follow this job’s steps in order. For each step: read the named `docs/tools/` file, write the produced file under this Work Item, run the listed check if present.
3. **journal-keeper** after each ready step (or after the whole named job if requested).

Initial phase for every job: first step in that workflow file.

## Jobs

- [Day List](day-list.md) — open the day (default)
- [Eligibility From Screenshot](eligibility-from-screenshot.md)
- [Intake Completeness](intake-completeness.md)
- [Wait List](wait-list.md)
- [Recall List If File](recall-list-if-file.md)
- [Referral Paperwork](referral-paperwork.md)
- [Records Release Log](records-release-log.md)
- [No Show List](no-show-list.md)
- [Day Close Tender](day-close-tender.md)

## Work map shape

Human notes go under the YAML block in each job file. Paths `work/` and `out/` mean **inside the current Work Item**.

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
| `id` | Step name |
| `needs` | Artifact ids that must already exist on disk under this Work Item |
| `produces` | Artifact id this step writes |
| `produce_path` | Path under `work/` or `out/` inside the Work Item |
| `tool` | File under `docs/tools/` to follow |
| `check` | Command that exits **0** if the step passed. If missing, ask before marking passed |
| `on_fail` | `retry` (at most 3) then ask |
| `next` | Step ids that may run after this one passes |

## Rules

- Do not start a step if any `needs` file is missing.
- Do not start a step that has no `check` without asking whether the produced file is enough.
- Do not mark the job done until every required produces file exists or an exception is documented.
