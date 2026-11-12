# Par Review

**When to use:** Compare their pars to the recent sales-mix export and to waste rows if those files exist. Do not change pars. List questions only: stale high pars on dead items, low pars that 86 often, weekend versus weekday mismatch. Do not 86 from mix alone. Do not invent a food-cost target. Theoretical usage is not a count. Menu changes stay the chef's. Say the date range on the mix. Starter par talk is not this shop's target until they teach.

**How to run:** Self-contained. Active Work Item under `work-items/<id>/`. For each ready step: read the tool doc → write `produce_path` inside that Work Item → run the check with working directory = the Work Item folder → journal-keeper. One **continue** = one ready step unless they asked to finish this job.

**Initial phase:** `mix`

## Work map

```yaml
id: par-review
steps:
  - id: mix
    needs: []
    produces: mix-raw
    produce_path: work/menu-mix.csv
    tool: docs/tools/pos-export.md
    check: python docs/tools/checks/csv-has-columns.py work/menu-mix.csv item qty
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [mix-raw]
    produces: par-pack
    produce_path: out/par-questions.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/par-questions.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator confirms how this kitchen files (`remember` / `integrate-docs`).
