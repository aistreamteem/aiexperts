# Role workflows

Named role jobs for the **Auto shop service advisor** Expert. Each job is registered in `workflow-registry.json` and has a YAML work map that **continue** walks. Do not skip a step with a chat summary. Data moves only as named files (`needs` / `produces`). Method: `docs/role/work-item-method.md`.

## Available workflows

Defined in `workflow-registry.json`. Default: `one-ro`.

1. **One RO** (`one-ro`) — One ticket write-up: concern in customer words, parts, estimate questions.
2. **Open ROs** (`open-ros`) — List open tickets from their board export or screenshot.
3. **MPI Pack** (`mpi-pack`) — Copy inspection tags and photo captions from their MPI export only.
4. **Estimate Pack** (`estimate-pack`) — Build estimate lines from their labor guide or menu plus confirmed parts.
5. **Auth Gap** (`auth-gap`) — Compare estimate lines to the authorization log; list pending lines.
6. **Additional Findings** (`additional-findings`) — New technician or MPI recommendations not yet authorized.
7. **Parts Status** (`parts-status`) — On order, in stock, backorder, and returned from vendor files and POs.
8. **Comeback** (`comeback`) — Match today's concern to a prior RO in their history export.
9. **Pickup Invoice** (`pickup-invoice`) — Compare last authorization and technician notes to the invoice PDF.

## How to run

1. Operator names a job, or **workflow-selector** records `Workflow type` from the registry.
2. Ensure a Work Item exists under `work-items/<id>/` with `in/`, `work/`, `out/`, `evidence/`.
3. **continue** one ready step (or the whole named job if requested). Rewrite `work/` and `out/` paths to that Work Item. Read the tool doc on the step. Produce the file. Run the check.
4. **journal-keeper** after the step.

**Initial phase** for every role job: `role-job`.

## Work map (required shape)

Put this YAML block in `.cursor/workflows/<id>.md`. Human notes go under it.

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
| `id` | Step name. Same idea as a pack **part**. |
| `needs` | Artifact ids that must already exist on disk under this Work Item. |
| `produces` | Artifact id this step writes. |
| `produce_path` | Path under `work/` (or `out/` for a finished pack), relative to `work-items/<id>/`. |
| `tool` | File under `docs/tools/` to follow. |
| `check` | Command that exits **0** if the step passed, **non-zero** if not. Required. |
| `on_fail` | `retry` (at most 3) then **ask**. |
| `next` | Step ids that may run after this one passes. A next step still waits until its `needs` exist. |

## Rules

- Do not start a step if any `needs` file is missing.
- Do not start a step that has no `check` — propose a check (they must approve) or **ask**.
- Do not mark the job done until every step has a passing check.

## Adding a role job

1. Add `.cursor/workflows/<id>.md` with **When to use**, **How to run**, **Initial phase** `role-job`, and the YAML work map.
2. Register it in `workflow-registry.json` (`instruction_file`, `initial_phase`: `role-job`).
3. Point `MyRole.txt`, `AGENTS.md`, and `docs/role/work-item-method.md` at the new file.

## Memory

Role facts and rules live in `facts/facts-operations.md` and `facts/rules-operations.md`.
