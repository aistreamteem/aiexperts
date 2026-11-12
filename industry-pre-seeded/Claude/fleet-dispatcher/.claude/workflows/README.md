# Role workflows

Named jobs for the **Fleet / delivery dispatcher** role. Each file is a self-contained instruction for **continue** / **workflow-selector**. Walk the YAML work map yourself. Do not skip a step with a chat summary. Data moves only as named files (`needs` / `produces`).

Jobs are listed in `workflow-registry.json`. Default workflow: `assignment-pack`. Method note: `docs/role/work-item-method.md`.

## How to run (every job)

1. Confirm or create a Work Item under `work-items/<id>/` (copy `work-items/_TEMPLATE/` if new). Put operator files in `in/`.
2. Load `facts/MEMORY-INDEX.md`, then shared then operations facts/rules, plus this Work Item’s facts/rules.
3. Walk the work map in the job file. One ready step per continue unless the operator asked for the whole named job.
4. Paths `work/` and `out/` mean inside the current Work Item folder. Read the named tool under `docs/tools/` and write `produce_path`.
5. A step passes only when its check command succeeds against those Work Item paths. On failure, retry at most 3 times, then ask with **operator-qa**. Do not invent a pass.
6. After each step, **journal-keeper**: `journals/work-items/<id>/progress.md` and `STATUS.md`.
7. Human gates: missing source files, assignment drafts, exception/breakdown language, HOS/fuel questions, and treating a pack as dispatched or billed wait for the operator. “Continue” is not approval.

Initial phase for every job: first ready YAML step (usually pull/list/units).

## Jobs

- [Assignment Pack](assignment-pack.md)
- [Breakdown](breakdown.md)
- [Detention](detention.md)
- [DVIR Gap](dvir-gap.md)
- [Exceptions](exceptions.md)
- [Fuel Outliers](fuel-outliers.md)
- [HOS Questions](hos-questions.md)
- [POD Check](pod-check.md)
- [Today's Routes](todays-routes.md)

## Work map shape

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
| `id` | Step name. |
| `needs` | Artifact ids that must already exist on disk under this Work Item. |
| `produces` | Artifact id this step writes. |
| `produce_path` | Path under this Work Item’s `work/` or `out/`. |
| `tool` | File under `docs/tools/` to follow. |
| `check` | Command that exits **0** if the step passed. Required. |
| `on_fail` | `retry` (at most 3) then **ask**. |
| `next` | Step ids that may run after this one passes. |

## Rules

- Do not start a step if any `needs` file is missing.
- Do not start a step that has no check — ask how they will know it is done.
- Do not mark the job done until every step has a passing check or a documented exception.
