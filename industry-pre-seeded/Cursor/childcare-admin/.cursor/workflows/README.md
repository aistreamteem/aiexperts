# Role workflows

Named jobs for the **Childcare center office (not the teacher)** role. Each file is a self-contained expert workflow with a YAML work map. **continue** walks one ready step. Do not skip a step with a chat summary. Data moves only as named files (`needs` / `produces`).

Jobs are listed in `workflow-registry.json`. Default workflow: `attendance-day`. Method: `docs/role/work-item-method.md`.

## How to run

1. Active Work Item under `work-items/<id>/` (**workflow-selector** / **continue** if needed)
2. Follow that job’s instruction file — one ready step (or the whole named job if requested)
3. **journal-keeper**

Relative `work/` and `out/` paths mean inside the current Work Item folder.

Initial phase for every job: `role-job` (role phases: intake → gather-sources → build-list → director-gate → pack-out).

## Jobs

- [Attendance Day](attendance-day.md)
- [Holiday Calendar Pack](holiday-calendar-pack.md)
- [Incident Routing](incident-routing.md)
- [Licensing Packet Completeness](licensing-packet-completeness.md)
- [Missing Enrollment Forms](missing-enrollment-forms.md)
- [Pickup List Check](pickup-list-check.md)
- [Ratio From Their Posted](ratio-from-their-posted.md)
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
```

| Field | Meaning |
| --- | --- |
| `id` | Step name. |
| `needs` | Artifact ids that must already exist on disk. |
| `produces` | Artifact id this step writes. |
| `produce_path` | Path under the Work Item `work/` (or `out/` for a finished pack). |
| `tool` | File under `docs/tools/` to follow. |
| `check` | Command that exits **0** if the step passed. Required. |
| `on_fail` | `retry` (at most 3) then **ask** with operator-qa. |
| `next` | Step ids that may run after this one passes. |

## Rules

- Do not start a step if any `needs` file is missing.
- Do not start a step that has no `check` — ask.
- Do not mark the job done until every step has a passing check or a documented exception.
