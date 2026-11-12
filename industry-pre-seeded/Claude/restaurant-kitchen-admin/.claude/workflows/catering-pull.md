# Catering Pull

**When to use:** Event pull for the date they name: extra prep and order qty from their BEO or pull sheet and from recipe yields they shared. Keep it off standing daily pars unless they already merge those files. Ask if event guest count or yield is missing. Do not invent covers. Do not 86 the dining-room dish because catering reserved product unless they said to. Leftover after the event follows their count rule. Do not invent donation legal status. One pack is one event date unless they asked otherwise.

**How to run:** Self-contained. Active Work Item under `work-items/<id>/`. For each ready step: read the tool doc → write `produce_path` inside that Work Item → run the check with working directory = the Work Item folder → journal-keeper. One **continue** = one ready step unless they asked to finish this job.

**Initial phase:** `pull`

## Work map

```yaml
id: catering-pull
steps:
  - id: pull
    needs: []
    produces: pull-raw
    produce_path: work/catering-pull.csv
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/csv-has-columns.py work/catering-pull.csv item qty
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [pull-raw]
    produces: pull-pack
    produce_path: out/catering-pull.md
    tool: docs/tools/recipe-file.md
    check: python docs/tools/checks/file-exists.py out/catering-pull.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator confirms how this kitchen files (`remember` / `integrate-docs`).
