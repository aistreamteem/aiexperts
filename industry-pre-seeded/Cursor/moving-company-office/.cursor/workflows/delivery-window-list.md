# Delivery window list

**When to use:** List dest windows and spreads from their calendar file and job sheet. Do not invent a clock hour or shrink a spread to look reliable. SIT or dest-TBD rows stay labeled; do not invent a street date. Missing windows on sold deliveries stay questions. They notify customers. You pack the list. Dest-agent names stay as filed, not a promised arrival.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put source files in `in/`. Walk one ready YAML step (or the whole named job if requested): read the named tool, produce the file, run the check, then **journal-keeper**. Do not invent weight, cube, rates, crew names, or delivery hours.

**Initial phase:** `role-job`

## Work map

```yaml
id: delivery-window-list
steps:
  - id: cal
    needs: []
    produces: cal
    produce_path: work/calendar.csv
    tool: docs/tools/calendar-file.md
    check: python docs/tools/checks/csv-has-columns.py work/calendar.csv job date
    on_fail: retry
    next: [jobs]
  - id: jobs
    needs: [cal]
    produces: jobs
    produce_path: work/jobs.csv
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/csv-has-columns.py work/jobs.csv job date
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [cal, jobs]
    produces: window-pack
    produce_path: out/delivery-windows.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/delivery-windows.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects this shop.
