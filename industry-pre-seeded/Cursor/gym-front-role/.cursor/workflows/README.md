# Role workflows

Named role jobs for **Gym / fitness front role**. Each job has a workflow file here and a matching entry in `workflow-registry.json`. Default workflow: `check-in-day`.

## How to run

Open or continue a Work Item under `work-items/<id>/`. Select the job with **workflow-selector** if needed. Follow this file’s YAML via **continue**: confirm `needs` exist, read the cited `docs/tools/` doc, write `produce_path` under the Work Item, run the step `check`, store the log in `evidence/`, then **journal-keeper**.

Initial phase for every job: `role-job`.

## Available jobs

1. **Check In Day** (`check-in-day`) — today’s check-in list from the scan export (typical daily job)
2. **Access Flag Exceptions** (`access-flag-exceptions`) — check-ins joined to the access-flag export
3. **Guest Pass Log** (`guest-pass-log`) — guest-pass log from check-ins and host rows
4. **Missing Waivers** (`missing-waivers`) — members and guests whose required form is absent
5. **Freeze And Cancel List** (`freeze-and-cancel-list`) — open freezes and pending cancels
6. **Failed Draft List** (`failed-draft-list`) — failed drafts from membership or billing export
7. **Class Roster** (`class-roster`) — roster from schedule plus check-ins or bookings
8. **PT Session Counts** (`pt-session-counts`) — purchased, used, and remaining PT sessions
9. **Retail Close** (`retail-close`) — retail close from count-and-price plus day-close tender

## Work map

The YAML block in each file is the source of truth for multi-step work. **continue** walks it. Do not skip a step with a chat summary. Data moves only as named files (`needs` / `produces`) under the active Work Item.

| Field | Meaning |
| --- | --- |
| `id` | Step name. Same idea as a work-map **part**. |
| `needs` | Artifact ids that must already exist on disk in this Work Item. |
| `produces` | Artifact id this step writes. |
| `produce_path` | Path under `work/` (or `out/` for a finished pack), relative to the Work Item. |
| `tool` | File under `docs/tools/` to follow. |
| `check` | Command that exits **0** if the step passed, **non-zero** if not. Required. |
| `on_fail` | `retry` (at most 3) then **ask**. |
| `next` | Step ids that may run after this one passes. A next step still waits until its `needs` exist. |

## Rules

- Do not start a step if any `needs` file is missing.
- Do not start a step that has no `check` — propose a check command and wait for operator approval, or **ask**.
- Do not mark the job done until every required step has a passing check (or a documented exception).

Human notes live under the YAML in each job file.
