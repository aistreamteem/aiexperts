# Role workflows

Named jobs for the **Purchasing / buyer (small manufacturer or shop)** role. Each file is a self-contained instruction for **continue** / **workflow-selector**: when to use it, how to run it, and a YAML work map. Do not skip a step with a chat summary. Data moves only as named files (`needs` / `produces`) under the current Work Item.

Jobs are listed in `workflow-registry.json`. Default workflow: `avl-check`.

Method: `docs/role/work-item-method.md`.

## How to run

1. Select the job (**workflow-selector**) and open `work-items/<id>/`
2. Put source files in `in/`
3. **continue** walks **one ready step** (or the whole named job if requested): read the tool doc, write the produced file, run the check, **journal-keeper**
4. On check fail, retry at most three times, then ask. If a step has no check, propose one and wait for approval

Initial phase for every job: first map step.

## Jobs

- [AVL Check](avl-check.md)
- [Backorder List](backorder-list.md)
- [Blanket Release](blanket-release.md)
- [Change Order Pack](change-order-pack.md)
- [Match](match.md)
- [Open POs](open-pos.md)
- [Quote Lead MOQ](quote-lead-moq.md)
- [Receiving Shorts](receiving-shorts.md)
- [RFQ From Files](rfq-from-files.md)

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
| `id` | Step name (a part of the pack). |
| `needs` | Artifact ids that must already exist on disk in this Work Item. |
| `produces` | Artifact id this step writes. |
| `produce_path` | Path under this Work Item `work/` or `out/`. |
| `tool` | File under `docs/tools/` to follow. |
| `check` | Command that exits **0** if the step passed, **non-zero** if not. Required. |
| `on_fail` | `retry` (at most 3) then **ask**. |
| `next` | Step ids that may run after this one passes. A next step still waits until its `needs` exist. |

## Rules

- Do not start a step if any `needs` file is missing.
- Do not start a step that has no `check` — propose a check, get approval, then save it, or ask.
- Do not mark the job done until every step has a passing check.
- Paths `work/` and `out/` mean **inside** `work-items/<id>/`.
