# Weather Postpone List

**When to use:** After they write a weather call, list postponed route stops and whether their note says next cycle or make-up. Do not cancel from radar. Do not invent a credit. Skips still win. Snow uses the snow file only if they have one. One property per row. They message customers. You pack leftovers from the route CSV plus the weather note. Missing tickets on leftover stops stay questions.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Follow this file's steps in order. Read the cited tool doc, write artifacts under that Work Item's `work/` and `out/`, run the listed check against those same paths, then **journal-keeper**. Do not invent a missing ticket, price, or weather call — ask with **operator-qa**.

**Initial phase:** `role-job`

## Work map

```yaml
id: weather-postpone-list
steps:
  - id: weather
    needs: []
    produces: weather
    produce_path: work/weather-note.md
    tool: docs/tools/weather-note.md
    check: python docs/tools/checks/file-exists.py work/weather-note.md
    on_fail: retry
    next: [route]
  - id: route
    needs: [weather]
    produces: route
    produce_path: work/route.csv
    tool: docs/tools/route-csv.md
    check: python docs/tools/checks/csv-has-columns.py work/route.csv route property
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [weather, route]
    produces: postpone-pack
    produce_path: out/weather-postpone.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/weather-postpone.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct shop practice (**remember** / **integrate-docs**).

