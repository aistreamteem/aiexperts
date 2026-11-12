# Role workflows

Named role jobs for **HOA / association admin**. Each job has a workflow file here and a matching entry in `workflow-registry.json`. Default workflow: `acc-completeness`. How a Work Item runs: `docs/role/work-item-method.md`.

## How to run

**workflow-selector** (if the Work Item has no Workflow type) → put operator files in the Work Item `in/` folder → **continue** walks one ready YAML step (or the whole named job if requested) → **journal-keeper**.

Initial phase for every job: `role-job` (see the method note: identify → intake → completeness → produce pack → human gate → close).

## Available jobs

1. **ACC Completeness** (`acc-completeness`) — missing pages, sketches, neighbor notes, and unsigned fields on the architectural application
2. **Bid Compare** (`bid-compare`) — amounts, allowances, exclusions, and dates from bid PDFs for one project
3. **Board Files** (`board-files`) — present-or-missing list of files for the next named meeting
4. **Dues Aging** (`dues-aging`) — current / 30 / 60 / 90+ balances from their ledger export
5. **Election Tally** (`election-tally`) — tally from the roster and ballot or proxy files they provide
6. **Reserve Index** (`reserve-index`) — reserve-study PDF present, cover date, association name, printed numbers they asked for
7. **Vendor Certs** (`vendor-certs`) — expiration dates, named insured, and additional-insured wording from filed certificates
8. **Violations** (`violations`) — open items, lots, categories, notice-step status, missing photos or blank lots
9. **Work Orders** (`work-orders`) — open common-area jobs, locations, vendors, and missing vendor or photo fields

## Work map

The YAML block in each file is the source of truth for multi-step work. **continue** walks it. Do not skip a step with a chat summary. Data moves only as named files (`needs` / `produces`). Paths are inside the current Work Item folder.

| Field | Meaning |
| --- | --- |
| `id` | Step name. Same idea as a **part**. |
| `needs` | Artifact ids that must already exist on disk from earlier steps. |
| `produces` | Artifact id this step writes. |
| `produce_path` | Path under `work/` (or `out/` for a finished pack). |
| `tool` | File under `docs/tools/` to follow. |
| `check` | Command that exits **0** if the step passed, **non-zero** if not. Required. |
| `on_fail` | `retry` (at most 3) then **ask**. |
| `next` | Step ids that may run after this one passes. A next step still waits until its `needs` exist. |

## Rules

- Do not start a step if any `needs` file is missing.
- Do not start a step that has no `check` — **ask**.
- Do not mark the job done until every step has a passing check.
- Human gates in `docs/role/work-item-method.md` are not passed by the word continue.

Human notes live under the YAML in each job file.
