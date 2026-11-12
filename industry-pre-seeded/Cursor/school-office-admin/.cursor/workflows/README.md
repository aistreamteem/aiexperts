# Role workflows

Named jobs for the **Small school office (not the teacher)** role. Each file is a self-contained work map for **continue** / **workflow-selector**. Data moves only as named files (`needs` / `produces`). Paths `in/`, `work/`, `out/`, and `evidence/` are inside `work-items/<id>/`.

Jobs are listed in `workflow-registry.json`. Default workflow: `attendance-day`. Method: `docs/role/work-item-method.md`.

## How to run

1. Open or continue a Work Item under `work-items/<id>/`. Put source files in that item’s `in/`.
2. Read the matching job file below and the named `docs/tools/` doc.
3. Walk **one ready YAML step** (or the whole named job if requested): produce the file, run the check, then **journal-keeper**.
4. Do not skip a step with a chat summary. If a `needs` file is missing, ask. Retry a failed check at most 3 times, then ask.

Initial phase for every job: isolate the Work Item, then walk the map.

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
| `needs` | Artifact ids that must already exist on disk in this Work Item. |
| `produces` | Artifact id this step writes. |
| `produce_path` | Path under `work/` (or `out/` for a finished pack) inside the Work Item. |
| `tool` | File under `docs/tools/` to follow. |
| `check` | Command that exits **0** if the step passed, **non-zero** if not. Required. |
| `on_fail` | `retry` (at most 3) then **ask**. |
| `next` | Step ids that may run after this one passes. A next step still waits until its `needs` exist. |

## Rules

- Do not start a step if any `needs` file is missing.
- Do not start a step that has no `check` — propose a check and wait for approval, or **ask**.
- Do not mark the job done until every step has a passing check.

## Adding a job

1. Add `.cursor/workflows/<id>.md` with **When to use**, **How to run**, and a work-map YAML block.
2. Register it in `workflow-registry.json` (job id = filename stem).
3. Point `MyRole.txt`, `AGENTS.md`, and `docs/role/work-item-method.md` at the new file.
