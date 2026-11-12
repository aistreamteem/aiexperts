# Truck calendar

**When to use:** List unit, date, and job from their truck calendar. Flag two firsts on one truck and jobs with no unit. Do not invent a free day or an empty weight. Shuttle units stay labeled if they coded them. Hired-hauler rows stay as they wrote them. They dispatch. You pack collisions and questions. Scale tickets are a different pack; do not fill tare from hope on this list.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put source files in `in/`. Walk one ready YAML step (or the whole named job if requested): read the named tool, produce the file, run the check, then **journal-keeper**. Do not invent weight, cube, rates, crew names, or delivery hours.

**Initial phase:** `role-job`

## Work map

```yaml
id: truck-calendar
steps:
  - id: trucks
    needs: []
    produces: trucks
    produce_path: work/truck-calendar.csv
    tool: docs/tools/truck-calendar.md
    check: python docs/tools/checks/csv-has-columns.py work/truck-calendar.csv truck date
    on_fail: retry
    next: [jobs]
  - id: jobs
    needs: [trucks]
    produces: jobs
    produce_path: work/jobs.csv
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/csv-has-columns.py work/jobs.csv job date
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [trucks, jobs]
    produces: truck-pack
    produce_path: out/truck-calendar.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/truck-calendar.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects this shop.
