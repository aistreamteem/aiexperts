# Role workflows

Named jobs for this Catering office role. Each job is an instruction file under `.claude/workflows/` and a matching key in `workflow-registry.json`. **continue** walks one ready step. Do not skip a step with a chat summary. Data moves only as named files (`needs` / `produces`).

Method: `docs/role/work-item-method.md`. Default job: `week-of-events`.

## How to run

This file is the whole job. **continue** and **workflow-selector** walk it. Do not look for deleted process skills.

1. Confirm or open a Work Item under `work-items/<id>/`. Record this job id as the workflow type.
2. Load `facts/MEMORY-INDEX.md`, then `facts/facts-operations.md` and `facts/rules-operations.md`.
3. Put operator files in `work-items/<id>/in/`. Working extracts go in `work/`. Finished packs go in `out/`. Check logs go in `evidence/`.
4. Read only the tool docs named in the steps below.
5. Walk the steps in order. Rewrite every `work/` and `out/` path so it sits under the Work Item folder. Do not start a step whose `needs` files are missing — ask.
6. After each step, run the listed check from the expert root with those rewritten paths. The step passes only when the check exits 0. On fail, retry at most 3 times, then ask. If a step has no check, propose a check and get operator approval before marking it passed.
7. Record progress with **journal-keeper**. Missing shop knowledge: ask; do not invent. Requests outside `MyRole.txt`: refuse and stop.
8. Job is done when every step has a passing check (or a documented exception), the pack exists under `out/`, and holes stay visible.

Initial phase for every role job: `role-job`.

## Registered jobs

| Job id | Instruction file | Phase it covers |
| --- | --- | --- |
| `week-of-events` | `.claude/workflows/week-of-events.md` | Week board / event identity |
| `count-vs-guarantee` | `.claude/workflows/count-vs-guarantee.md` | Final count |
| `dietary-list` | `.claude/workflows/dietary-list.md` | Dietary / allergen routing |
| `pack-out-list` | `.claude/workflows/pack-out-list.md` | Production pack-out |
| `equipment-vs-events` | `.claude/workflows/equipment-vs-events.md` | House kit vs same-day events |
| `rental-pos` | `.claude/workflows/rental-pos.md` | Rental POs |
| `staffing-from-file` | `.claude/workflows/staffing-from-file.md` | Labor grid |
| `change-after-cutoff-log` | `.claude/workflows/change-after-cutoff-log.md` | Late revisions |
| `leftover-form-completeness` | `.claude/workflows/leftover-form-completeness.md` | Leftover-release completeness |

Skip `README.md` and any `_example-*.md`. Those are not live jobs.

## Work map (required shape)

Put this YAML block in `.claude/workflows/<name>.md` under **Work map**. Human notes go under it.

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
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/done-file.md
    on_fail: retry
    next: []
```

| Field | Meaning |
| --- | --- |
| `id` | Step name. Same idea as a catering-job **part**. |
| `needs` | Artifact ids that must already exist on disk under the Work Item. |
| `produces` | Artifact id this step writes. |
| `produce_path` | Path under `work/` (or `out/` for a finished pack), inside the Work Item folder. |
| `tool` | File under `docs/tools/` to follow. |
| `check` | Command that exits **0** if the step passed, **non-zero** if not. Required. |
| `on_fail` | `retry` (at most 3) then **ask**. |
| `next` | Step ids that may run after this one passes. A next step still waits until its `needs` exist. |

Register each new job in `workflow-registry.json` (job id = filename stem). Memory for this role: `facts/facts-operations.md` and `facts/rules-operations.md`.

## Rules

- Do not start a step if any `needs` file is missing.
- Do not start a step that has no `check` — propose a check (they must approve) or **ask**.
- Do not mark the job done until every step has a passing check (or a documented exception).
