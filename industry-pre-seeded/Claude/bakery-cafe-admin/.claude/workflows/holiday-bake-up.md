# Holiday Bake Up

**When to use:** Pull the holiday tab on their calendar and the matching bake-list rows: pies, cookies, laminated locks, preorder cutoffs. Do not invent holiday qty from last year. Do not invent a seasonal formula. Do not leave holiday qty on the next daily list unless they said so. Flag ingredient and oven-window holes. The pack is the dated plan plus asks. They own the holiday.

**How to run:** Self-contained. Active Work Item under `work-items/<id>/`. For each ready step: read the tool doc → write `produce_path` inside that Work Item → run the check with working directory = the Work Item folder → journal-keeper.

**Initial phase:** `cal`

## Work map

```yaml
id: holiday-bake-up
steps:
  - id: cal
    needs: []
    produces: cal
    produce_path: work/production-calendar.csv
    tool: docs/tools/calendar.md
    check: python docs/tools/checks/file-exists.py work/production-calendar.csv
    on_fail: retry
    next: [list]
  - id: list
    needs: [cal]
    produces: bake-list
    produce_path: work/bake-list.csv
    tool: docs/tools/bake-list-sheet.md
    check: python docs/tools/checks/file-exists.py work/bake-list.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [cal, bake-list]
    produces: holiday-pack
    produce_path: out/holiday-bake-up.md
    tool: docs/tools/calendar.md
    check: python docs/tools/checks/file-exists.py out/holiday-bake-up.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator confirms how this shop files (`remember` / `integrate-docs`).
