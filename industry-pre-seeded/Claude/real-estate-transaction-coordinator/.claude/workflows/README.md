# Role workflows

Named jobs for the **Real estate transaction coordinator** role. Each file is a self-contained expert workflow with a YAML work map. `continue` walks the map. Do not skip a step with a chat summary. Data moves only as named files (`needs` / `produces`).

Jobs are listed in `workflow-registry.json`. Default workflow: `dates-calendar`. Method: `docs/role/work-item-method.md`.

## How to run

1. Open or select a Work Item under `work-items/<id>/` (`workflow-selector` if needed)
2. Follow this job file one ready step (or the whole named job if requested)
3. `journal-keeper` after each step

Initial phase for every job: `role-job`.

## Jobs

- [Dates Calendar](dates-calendar.md)
- [Missing Docs](missing-docs.md)
- [Disclosure Completeness](disclosure-completeness.md)
- [Option Period Pack](option-period-pack.md)
- [Inspection to Repair Amendment Log](inspection-to-repair-amendment-log.md)
- [Amendment Log Pack](amendment-log-pack.md)
- [HOA Packet Completeness](hoa-packet-completeness.md)
- [Closing Checklist](closing-checklist.md)
- [Wire Fraud Checklist as Their Process](wire-fraud-checklist-as-their-process.md)

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
| `produce_path` | Path under `work/` (or `out/` for a finished pack), relative to the Work Item root. |
| `tool` | File under `docs/tools/` to follow. |
| `check` | Command that exits **0** if the step passed, **non-zero** if not. Required. |
| `on_fail` | `retry` (at most 3) then ask. |
| `next` | Step ids that may run after this one passes. A next step still waits until its `needs` exist. |

## Rules

- Do not start a step if any `needs` file is missing.
- Do not start a step that has no `check` — ask.
- Do not mark the job done until every step has a passing check.
- Paths `work/` and `out/` mean inside `work-items/<id>/`.
