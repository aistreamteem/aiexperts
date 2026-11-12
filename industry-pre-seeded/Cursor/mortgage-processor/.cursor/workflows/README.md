# Role workflows

Named jobs for **Mortgage processor (file completeness)**. Each job is a registry entry in `workflow-registry.json` and a work map in this folder. **continue** walks the YAML one ready step at a time. Do not skip a step with a chat summary. Data moves only as named files (**needs** / **produces**).

Default job: `conditions-checklist`.

Method: `docs/role/work-item-method.md`.

## How to run

1. Open or select a Work Item under `work-items/<id>/` (`continue` / **workflow-selector**).
2. Follow this file one ready step (or the whole named job if they asked).
3. **journal-keeper** after the step.

Initial phase for every job: `role-job`.

## Jobs

| Id | File |
| --- | --- |
| conditions-checklist | [conditions-checklist.md](conditions-checklist.md) |
| loan-file-index | [loan-file-index.md](loan-file-index.md) |
| missing-docs | [missing-docs.md](missing-docs.md) |
| date-stamps | [date-stamps.md](date-stamps.md) |
| appraisal-in-file-not-value | [appraisal-in-file-not-value.md](appraisal-in-file-not-value.md) |
| title-routing | [title-routing.md](title-routing.md) |
| insurance-binder-present | [insurance-binder-present.md](insurance-binder-present.md) |
| cd-le-present | [cd-le-present.md](cd-le-present.md) |
| suspense-list-as-their-codes | [suspense-list-as-their-codes.md](suspense-list-as-their-codes.md) |
| wire-fraud-checklist-their-process | [wire-fraud-checklist-their-process.md](wire-fraud-checklist-their-process.md) |

## Work map shape

Each job file has title, **When to use**, **How to run**, **Initial phase**, then this YAML (human notes go under it):

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
| `needs` | Artifact ids that must already exist on disk under this Work Item. |
| `produces` | Artifact id this step writes. |
| `produce_path` | Path under `work/` (or `out/` for a finished pack), relative to the Work Item root. |
| `tool` | File under `docs/tools/` to follow. |
| `check` | Command that exits **0** if the step passed, **non-zero** if not. Required. |
| `on_fail` | `retry` (at most 3) then **ask**. |
| `next` | Step ids that may run after this one passes. A next step still waits until its `needs` exist. |

## Rules

- Do not start a step if any `needs` file is missing.
- Do not start a step that has no `check` — propose a check, wait for operator approval, then save it.
- Do not mark the job done until every step has a passing check.
- New job stubs go here and get a matching key in `workflow-registry.json`. Do not add a developer pipeline.
