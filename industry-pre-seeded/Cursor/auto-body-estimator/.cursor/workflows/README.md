# Role workflows

Named role jobs for **Auto body estimator / office**. Each job has a workflow file here and a matching entry in `workflow-registry.json`. Default workflow: `assignment-intake`.

Role method: `docs/role/work-item-method.md`.

## How to run

Confirm a Work Item under `work-items/<id>/` → **continue** walks one ready YAML step (or the whole named job if requested) → write under that Work Item’s `in/`, `work/`, `out/`, `evidence/` → **journal-keeper**.

If the journal has no workflow type, **workflow-selector** offers the registry list.

Initial phase is the first YAML step in the selected file.

## Available jobs

1. **Assignment Intake** (`assignment-intake`) — intake pack from assignment sheet and VIN file
2. **Authorization Missing** (`authorization-missing`) — estimate dollars versus saved portal or signed auth
3. **Customer Pay Vs Insurer** (`customer-pay-vs-insurer`) — split lines by insurer, deductible, and customer-pay
4. **Cycle Time List** (`cycle-time-list`) — stage dates from cycle calendar joined to open estimates
5. **Estimate From Files** (`estimate-from-files`) — estimate pack from labor matrix, parts file, and export
6. **OEM Procedure Present** (`oem-procedure-present`) — procedure PDFs versus estimate operations
7. **Parts Order Vs Estimate** (`parts-order-vs-estimate`) — parts PO sheet joined to estimate lines
8. **Photo Index** (`photo-index`) — photo folder index plus required-angle asks
9. **Supplement Log** (`supplement-log`) — estimate versions and first-write versus later dollars

## Work map

The YAML block in each file is the source of truth for multi-step work. **continue** walks it. Do not skip a step with a chat summary. Data moves only as named files (`needs` / `produces`).

| Field | Meaning |
| --- | --- |
| `id` | Step name. |
| `needs` | Artifact ids that must already exist on disk under this Work Item. |
| `produces` | Artifact id this step writes. |
| `produce_path` | Path under this Work Item’s `work/` (or `out/` for a finished pack). |
| `tool` | File under `docs/tools/` to follow. |
| `check` | Command that exits **0** if the step passed, **non-zero** if not. Required. Paths are relative to the Work Item folder. |
| `on_fail` | `retry` (at most 3) then **ask**. |
| `next` | Step ids that may run after this one passes. A next step still waits until its `needs` exist. |

## Rules

- Do not start a step if any `needs` file is missing.
- Do not start a step that has no `check` — ask how to prove it, and only add a check after the operator approves.
- Do not mark the job done until every step has a passing check or a documented exception in `evidence/` and the journal.

Human notes live under the YAML in each job file.
