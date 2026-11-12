# Role workflows

Named jobs for the **Physical therapy front role (not the therapist)** role. Each file is an expert workflow with a YAML work map. **continue** walks the map. Do not skip a step with a chat summary. Data moves only as named files (`needs` / `produces`).

Jobs are listed in `workflow-registry.json`. Default workflow: `auth-remaining-from-file`. Method: `docs/role/work-item-method.md`.

## How to run

1. Open or switch to a Work Item under `work-items/<id>/` (**workflow-selector** if the job is new).
2. Follow the YAML with **continue** — one ready step (or the whole named job if requested).
3. Read the named `docs/tools/` file. Write artifacts under this Work Item. Run each step’s check.
4. **journal-keeper** after the step.

Initial phase for every job: `role-job`.

## Jobs

- [Auth Remaining From File](auth-remaining-from-file.md)
- [Day Close](day-close.md)
- [Day List](day-list.md)
- [HEP Print Index](hep-print-index.md)
- [No Show List](no-show-list.md)
- [Recert Dates](recert-dates.md)
- [Referral POC Completeness](referral-poc-completeness.md)
- [Visit Count Export Check](visit-count-export-check.md)
- [Wait List](wait-list.md)

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
| `id` | Step name. Same idea as a **part** of the job. |
| `needs` | Artifact ids that must already exist on disk in this Work Item. |
| `produces` | Artifact id this step writes. |
| `produce_path` | Path under `work/` (or `out/` for a finished pack). Relative to the Work Item folder. |
| `tool` | File under `docs/tools/` to follow. |
| `check` | Command that exits **0** if the step passed, **non-zero** if not. Required. |
| `on_fail` | `retry` (at most 3) then **ask**. |
| `next` | Step ids that may run after this one passes. A next step still waits until its `needs` exist. |

## Rules

- Do not start a step if any `needs` file is missing.
- Do not start a step that has no `check` — propose a check command (they must approve) or **ask**.
- Do not mark the job done until every step has a passing check.
