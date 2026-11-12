# Role workflows

Named jobs for the **Hotel / inn front role**. Each job is its own instruction file under this folder and a key in `workflow-registry.json`. **continue** walks one ready step. Do not skip a step with a chat summary. Data moves only as named files (`needs` / `produces`) under the active Work Item.

Default workflow: `arrivals-day`. Method: `docs/role/work-item-method.md`.

## Available jobs

1. **Arrivals Day** (`arrivals-day`) — Build today's arrivals list from their CSV and mark ready versus not-ready using the room-status sheet.
2. **Departures Due Out** (`departures-due-out`) — List due-outs and planned departures from the in-house export and room status.
3. **Folio Exceptions** (`folio-exceptions`) — Read folio PDFs against the tax file and list missing posts, duplicates, and tax-off without a cert.
4. **Group Block Vs Pickup** (`group-block-vs-pickup`) — Compare contracted block rooms to pickup on their group sheet and the arrivals export.
5. **House Count** (`house-count`) — Restate tonight's house count from their PMS export and in-house list.
6. **Night Audit File Check** (`night-audit-file-check`) — Check that the night-audit packet they dropped has the usual pages versus their PMS export.
7. **No Show List** (`no-show-list`) — Build the no-show list from arrivals that did not check in and from the night-audit PDF if it already coded them.
8. **Ooo And Status** (`ooo-and-status`) — List out-of-order and status-board rooms from their status sheet and the PMS export.
9. **Tax Exempt Completeness** (`tax-exempt-completeness`) — Compare folios coded tax-exempt to certificates in the tax-file folder.

## How to run

1. **workflow-selector** (or an already-named job) + an active folder under `work-items/<id>/`.
2. Put source files in that Work Item’s `in/`. Load operations memory.
3. Follow the matching `.claude/workflows/<id>.md` file. One ready step per **continue** unless they asked for the whole named job.
4. **journal-keeper** after the step.

`continue` means one ready workflow step. It is not approval of an open question.

**Initial phase** for every role job: identify / intake, then the steps in that file.

These files are self-contained. They do not require deleted process skills.

## Step list (required shape)

Put a YAML block in `.claude/workflows/<name>.md` under **Work map** so **continue** can see needs / produces / check. Human notes go above it. Register the job in `workflow-registry.json`. Paths are relative to `work-items/<id>/`.

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
| `id` | Step name (a part of the job). |
| `needs` | Artifact ids that must already exist on disk under this Work Item. |
| `produces` | Artifact id this step writes. |
| `produce_path` | Path under `work/` (or `out/` for a finished pack), relative to the Work Item. |
| `tool` | File under `docs/tools/` to follow. |
| `check` | Command that exits **0** if the step passed. Required. Run with cwd or paths inside the Work Item. |
| `on_fail` | `retry` (at most 3) then **ask**. |
| `next` | Step ids that may run after this one passes. |

## Rules

- Do not start a step if any `needs` file is missing.
- Do not start a step that has no `check` — ask how to know it passed. Do not mark it passed.
- Do not mark the job done until every step has a passing check or a documented exception.

## Adding a role job

1. Add `.claude/workflows/<id>.md` with **When to use**, **How to run**, and the step list.
2. Register it in `workflow-registry.json`.
3. Point `MyRole.txt`, `CLAUDE.md`, and `docs/role/work-item-method.md` at the new file.

Expert-role memory for this role: `facts/facts-operations.md` and `facts/rules-operations.md`.
