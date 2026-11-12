# Role workflows

Named jobs for the **Small school office (not the teacher)** role. Each file is an expert workflow with a YAML work map. **continue** walks the map (one ready step, or the whole named job if requested). Do not skip a step with a chat summary. Data moves only as named files (`needs` / `produces`).

Jobs are listed in `workflow-registry.json`. Default workflow: `attendance-day`. Method: `docs/role/work-item-method.md`.

## How to run

1. Open or switch to a Work Item under `work-items/<id>/` (**workflow-selector** if the job is new)
2. Follow the selected `.claude/workflows/<job>.md` YAML — one ready step (or the whole named job if requested)
3. Read the named `docs/tools/` file, write `produce_path` inside this Work Item, run `check` against those paths
4. **journal-keeper**

Initial phase for every job: isolate / intake, then the first YAML step.

## Jobs

- [Attendance Day](attendance-day.md)
- [Calendar Pack](calendar-pack.md)
- [Immunization Present Missing](immunization-present-missing.md)
- [Missing Enrollment](missing-enrollment.md)
- [Pickup List](pickup-list.md)
- [Records Request Completeness](records-request-completeness.md)
- [Transcript Request Log](transcript-request-log.md)
- [Tuition From File](tuition-from-file.md)
- [Waitlist](waitlist.md)

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
| `id` | Step name. Same idea as a **part**. |
| `needs` | Artifact ids that must already exist on disk in this Work Item. |
| `produces` | Artifact id this step writes. |
| `produce_path` | Path under `work/` (or `out/` for a finished pack) **inside the current Work Item**. |
| `tool` | File under `docs/tools/` to follow. |
| `check` | Command that exits **0** if the step passed, **non-zero** if not. Required. |
| `on_fail` | `retry` (at most 3) then **ask**. |
| `next` | Step ids that may run after this one passes. A next step still waits until its `needs` exist. |

## Rules

- Do not start a step if any `needs` file is missing.
- Do not start a step that has no `check` — propose a check command (they must approve) or **ask**.
- Do not mark the job done until every step has a passing check.
- Paths `in/`, `work/`, `out/`, and `evidence/` mean **inside `work-items/<id>/`**.
