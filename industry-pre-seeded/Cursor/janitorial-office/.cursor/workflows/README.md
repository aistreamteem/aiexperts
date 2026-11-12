# Role workflows

Named jobs for the **Janitorial / contract-cleaning office** role. Each file is a self-contained instruction for **continue** / **workflow-selector**. Follow the steps in order: read the tool doc, produce the artifact under the active Work Item (`work-items/<id>/`), run the check, retry at most three times then ask, then **journal-keeper**.

Jobs are listed in `workflow-registry.json`. Default workflow: `complaint-callback`. Recurring nightly assignment is usually `night-board`.

## How to run

1. Open or use the active Work Item under `work-items/<id>/` (create `in/`, `work/`, `out/`, `evidence/` if missing)
2. Follow the selected `.cursor/workflows/<job>.md` one ready step (or the whole named job if requested)
3. Paths in each step are **inside that Work Item folder**
4. **journal-keeper** after each step

Initial phase for every job: first step in that file.

## Jobs

- [Complaint Callback](complaint-callback.md)
- [Extra Work Auth List](extra-work-auth-list.md)
- [Holiday Coverage](holiday-coverage.md)
- [Key Log Completeness](key-log-completeness.md)
- [Missed Service List](missed-service-list.md)
- [Night Board](night-board.md)
- [Quality Checklist Pack](quality-checklist-pack.md)
- [SDS Index Missing](sds-index-missing.md)
- [Supply Below Par](supply-below-par.md)

## Work map shape

The YAML block is the step list. **continue** walks it directly. Human notes sit above the YAML.

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
| `id` | Step name |
| `needs` | Artifact ids that must already exist on disk under this Work Item |
| `produces` | Artifact id this step writes |
| `produce_path` | Path under `work/` (or `out/` for a finished pack), relative to the Work Item |
| `tool` | File under `docs/tools/` to follow |
| `check` | Command that exits **0** if the step passed. Run it with Work Item-relative paths. |
| `on_fail` | `retry` (at most 3) then **ask** |
| `next` | Step ids that may run after this one passes |

## Rules

- Do not start a step if any `needs` file is missing.
- Do not start a step that has no `check` — propose a check and get approval, or ask.
- Do not mark the job done until every step has a passing check or a documented exception.
- Do not invent missing shop data. Human gates live in `docs/role/work-item-method.md`.
