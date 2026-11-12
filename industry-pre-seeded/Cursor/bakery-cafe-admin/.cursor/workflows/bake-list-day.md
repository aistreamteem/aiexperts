# Bake List Day

**When to use:** Build the day's bake plan from their bake-list sheet and formula file: item, mix count, cafe versus wholesale split, and missing formula pointers. Do not invent a formula or a mix count. Do not treat this as restaurant line tickets. Flag when case or standing demand is named on the list but yield is missing. The pack is the plan plus asks. They mix and bake.

**How to run:** Self-contained. Active Work Item under `work-items/<id>/`. For each ready step: read the tool doc → write `produce_path` inside that Work Item → run the check with working directory = the Work Item folder → journal-keeper. One **continue** = one ready step unless they asked to finish this job. Missing formula pointers are a human gate, not a number you fill.

**Initial phase:** `list`

## Work map

```yaml
id: bake-list-day
steps:
  - id: list
    needs: []
    produces: bake-list
    produce_path: work/bake-list.csv
    tool: docs/tools/bake-list-sheet.md
    check: python docs/tools/checks/csv-has-columns.py work/bake-list.csv item qty
    on_fail: retry
    next: [formulas]
  - id: formulas
    needs: [bake-list]
    produces: formulas
    produce_path: work/formula-index.csv
    tool: docs/tools/formula-file.md
    check: python docs/tools/checks/file-exists.py work/formula-index.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [bake-list, formulas]
    produces: bake-pack
    produce_path: out/bake-list-day.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/bake-list-day.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator confirms how this shop files (`remember` / `integrate-docs`).
