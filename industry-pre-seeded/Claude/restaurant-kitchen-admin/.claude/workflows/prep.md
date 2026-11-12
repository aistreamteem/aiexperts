# Prep

**When to use:** Prep list for the next shift they name (AM, PM, brunch, or close). Prep qty is par minus on-hand when both exist, rounded to their batch if the recipe card says so. Put 86 on top if they 86'd a finished dish or a component; do not cancel every sub-recipe unless they said to. Do not apply dinner pars to lunch. Do not compute if on-hand is missing. Yield numbers come from the card they shared; secret recipes stay unpublished. Name the shift on the pack.

**How to run:** Self-contained. Active Work Item under `work-items/<id>/`. For each ready step: read the tool doc → write `produce_path` inside that Work Item → run the check with working directory = the Work Item folder → journal-keeper. One **continue** = one ready step unless they asked to finish this job.

**Initial phase:** `list`

## Work map

```yaml
id: prep
steps:
  - id: list
    needs: []
    produces: prep
    produce_path: work/prep.csv
    tool: docs/tools/prep-sheet.md
    check: python docs/tools/checks/csv-has-columns.py work/prep.csv item prep_qty
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [prep]
    produces: prep-pack
    produce_path: out/prep.md
    tool: docs/tools/prep-sheet.md
    check: python docs/tools/checks/file-exists.py out/prep.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator confirms how this kitchen files (`remember` / `integrate-docs`).
