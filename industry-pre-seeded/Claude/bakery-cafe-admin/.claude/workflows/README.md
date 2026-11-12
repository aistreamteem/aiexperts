# Role workflows

Named jobs for the **Bakery / cafe production office**. Each file is a self-contained instruction for **continue** / **workflow-selector**. **continue** walks one ready step. Do not skip a step with a chat summary. Data moves only as named files (`needs` / `produces`).

Jobs are listed in `workflow-registry.json`. Default daily job: `bake-list-day`. Role method: `docs/role/work-item-method.md`.

## How to run

1. Have an active Work Item under `work-items/<id>/` (`in/`, `work/`, `out/`, `evidence/`). Use **workflow-selector** if none is active.
2. Read the current step in this file. Read the cited `docs/tools/` doc.
3. Write the artifact to `produce_path` **inside the Work Item folder**.
4. Run the listed `check` with working directory = the Work Item folder. Exit 0 = pass. On fail, retry at most 3 times from the tool doc, then ask via **operator-qa**. Never invent a pass.
5. **journal-keeper**.

Initial phase for every job: the first YAML step id.

## Jobs

- [Bake List Day](bake-list-day.md) — default daily job
- [Case Par Vs Count](case-par-vs-count.md)
- [Wholesale Day](wholesale-day.md)
- [Custom Cake Board](custom-cake-board.md)
- [Holiday Bake Up](holiday-bake-up.md)
- [Receiving Shorts](receiving-shorts.md)
- [Ingredient Below Par](ingredient-below-par.md)
- [Stale And Waste](stale-and-waste.md)
- [Allergen Sheet Index](allergen-sheet-index.md)

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
| `needs` | Artifact ids that must already exist on disk in this Work Item. |
| `produces` | Artifact id this step writes. |
| `produce_path` | Path under `work/` or `out/` inside the Work Item. |
| `tool` | File under `docs/tools/` to follow. |
| `check` | Command that exits **0** if the step passed. |
| `on_fail` | `retry` (at most 3) then ask. |
| `next` | Step ids that may run after this one passes. |

## Rules

- Do not start a step if any `needs` file is missing.
- Do not start a step that has no `check` — ask how they will know it passed.
- Do not mark the job done until every step has a passing check or a documented visible exception.
- Quantities quote their files. Shorts, stales, missing formulas, and blank allergen cells stay visible.
