# Role workflows

Named jobs for the **Nonprofit office admin**. Each job is its own expert workflow under this folder and a key in `workflow-registry.json`. **continue** walks the YAML work map in the matching file. Do not skip a step with a chat summary. Data moves only as named files (`needs` / `produces`). Paths `work/` and `out/` mean inside `work-items/<id>/`.

Method: `docs/role/work-item-method.md`. Default workflow: `board-pack`.

## Available jobs

1. **Board Pack** (`board-pack`) — Agenda, exhibits, treasurer attachments, and minutes index for the named meeting date.
2. **Donor List** (`donor-list`) — Filter the donor export and list holes; they communicate, you do not send.
3. **Funder Gap** (`funder-gap`) — Mark required award attachments present or missing in the grant folder.
4. **Gift Ack Draft** (`gift-ack-draft`) — Draft acknowledgment letters from their template and gift file; they send and sign.
5. **Grant Deadlines** (`grant-deadlines`) — List upcoming reports, draws, and closeouts from the grants sheet versus the award PDF.
6. **Grant Report** (`grant-report`) — Map funder template questions to program files and the award-coded financial export.
7. **In Kind List** (`in-kind-list`) — List in-kind log rows without fair-market values, wages, or deductibility opinions.
8. **Minutes Index** (`minutes-index`) — Index meeting dates and draft versus adopted minutes from their folder.
9. **Restricted Ask** (`restricted-ask`) — List uncoded, ambiguous, leftover, or mislabeled restricted-fund rows for the bookkeeper.

## How to run

1. Load shared memory (`facts/MEMORY-INDEX.md`, then the shared pair). Match the request to a job in `workflow-registry.json` (**workflow-selector** if the journal has no Workflow type).
2. Confirm a Work Item folder under `work-items/<id>/` (`in/`, `work/`, `out/`, `evidence/`).
3. Follow this job’s markdown: one ready YAML step (or the whole named job if they asked).
4. **journal-keeper** after the step.

`continue` means one ready work-map step. It is not approval of an open question.

**Initial phase** for every role job: first ready YAML step (intake / pull).

## Work map (required shape)

Put this YAML block in `.claude/workflows/<name>.md` under **Work map**. Human notes go under it. Register the job in `workflow-registry.json`. `produce_path` and `check` paths are relative to the Work Item folder.

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
| `needs` | Artifact ids that must already exist on disk in this Work Item. |
| `produces` | Artifact id this step writes. |
| `produce_path` | Path under this Work Item’s `work/` or `out/`. |
| `tool` | File under `docs/tools/` to follow. |
| `check` | Command that exits **0** if the step passed. Required. Run it against this Work Item’s paths. |
| `on_fail` | `retry` (at most 3) then **ask**. |
| `next` | Step ids that may run after this one passes. A next step still waits until its `needs` exist. |

## Rules

- Do not start a step if any `needs` file is missing.
- Do not start a step that has no `check` — **ask** how they will know it is done.
- Do not mark the job done until every step has a passing check, or a documented exception is in the journal.
- They circulate, sign, send, and submit. Drafts in `out/` are not issued.

## Adding a role job

1. Add `.claude/workflows/<id>.md` with **When to use**, **How to run**, and the YAML work map. Keep instructions self-contained (this file plus listed tools).
2. Register it in `workflow-registry.json`.
3. Point `MyRole.txt` and `CLAUDE.md` at the new file. Update `docs/role/work-item-method.md`.

Expert-role memory for this role: `facts/facts-shared.md` and `facts/rules-shared.md`.
