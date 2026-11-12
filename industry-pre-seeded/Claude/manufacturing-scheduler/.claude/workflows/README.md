# Role workflows

Named jobs for the **Small-plant production scheduler** role. Each file is a self-contained instruction with a YAML work map. **continue** walks one ready step. Do not skip a step with a chat summary. Data moves only as named files (`needs` / `produces`). Method: `docs/role/work-item-method.md`.

Jobs are listed in `workflow-registry.json`. Default workflow: `dispatch-list`.

## How to run

1. Open or continue a Work Item under `work-items/<id>/` (**workflow-selector** if the job is not chosen yet).
2. Put source exports in `in/`.
3. Walk the selected `.claude/workflows/<job>.md` one ready step (or the whole named job if requested): read the cited `docs/tools/` file, write `produce_path` inside this Work Item, run the check, log `evidence/`, **journal-keeper**.
4. Paths `work/` and `out/` mean inside the current Work Item folder.

Initial phase for every job: intake, then the steps in that file.

## Jobs

- [Dispatch List](dispatch-list.md)
- [Due Date List](due-date-list.md)
- [Pending ECO as File](eco-pending-as-file.md)
- [Kit List](kit-list.md)
- [Machine-Down versus WIP](machine-down-vs-wip.md)
- [Outside-Process Due List](outside-process-due.md)
- [Shortage List versus Inventory](shortage-vs-inventory.md)
- [Traveler Completeness Pack](traveler-completeness.md)
- [WIP by Work Center](wip-by-center.md)

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
| `produce_path` | Path under `work/` (or `out/` for a finished pack), relative to the Work Item. |
| `tool` | File under `docs/tools/` to follow. |
| `check` | Command that exits **0** if the step passed, **non-zero** if not. Required. |
| `on_fail` | `retry` (at most 3) then **ask**. |
| `next` | Step ids that may run after this one passes. A next step still waits until its `needs` exist. |

## Rules

- Do not start a step if any `needs` file is missing.
- Do not start a step that has no `check` — propose a check and obtain approval, or **ask**.
- Do not mark the job done until every step has a passing check or a documented exception.

