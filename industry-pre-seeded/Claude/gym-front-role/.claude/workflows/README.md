# Role workflows

Named jobs for the **Gym / fitness front role**. Each file is a self-contained work map. **continue** walks the next ready step. Do not skip a step with a chat summary. Data moves only as named files (`needs` / `produces`). Paths `work/` and `out/` are inside the active Work Item folder (`work-items/<id>/`).

Jobs are listed in `workflow-registry.json`. Default workflow: `check-in-day`. Method: `docs/role/work-item-method.md`.

## How to run

1. Open or reuse a Work Item under `work-items/<id>/` (**workflow-selector** if the job is unset)
2. Follow this file via **continue**: one ready step (or the whole named job if requested)
3. **journal-keeper** after the step

Initial phase for every job: `intake`, then the first YAML step.

## Jobs

- [Check In Day](check-in-day.md) — typical daily job
- [Access Flag Exceptions](access-flag-exceptions.md)
- [Guest Pass Log](guest-pass-log.md)
- [Missing Waivers](missing-waivers.md)
- [Freeze And Cancel List](freeze-and-cancel-list.md)
- [Failed Draft List](failed-draft-list.md)
- [Class Roster](class-roster.md)
- [Pt Session Counts](pt-session-counts.md)
- [Retail Close](retail-close.md)

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
| `id` | Step name. |
| `needs` | Artifact ids that must already exist on disk under the Work Item. |
| `produces` | Artifact id this step writes. |
| `produce_path` | Path under the Work Item `work/` (or `out/` for a finished pack). |
| `tool` | File under `docs/tools/` to follow. |
| `check` | Command that exits **0** if the step passed, **non-zero** if not. Required. |
| `on_fail` | `retry` (at most 3) then **ask**. |
| `next` | Step ids that may run after this one passes. A next step still waits until its `needs` exist. |

## Rules

- Do not start a step if any `needs` file is missing.
- Do not start a step that has no `check` — propose a check and get approval, or **ask**.
- Do not mark the job done until every step has a passing check (or a documented exception the operator accepted).
