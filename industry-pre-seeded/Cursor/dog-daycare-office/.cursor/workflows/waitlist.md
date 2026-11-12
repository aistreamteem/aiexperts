# Waitlist

**When to use:** From their waitlist sheet and calendar, list order, requested dates, and stay type. Do not jump a row. Do not confirm a stay unless they asked you to draft from their process. Do not invent a peak deposit. Vaccine-file and waiver gates stay present or missing, never a medical due-date. You do not message the list as a blast. Starter / guess until they teach the sort key and who calls the next name.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put source files in `in/`. Walk one ready YAML step (or the whole named job if requested): read the named tool doc, produce the file, run the check, then **journal-keeper**.

**Initial phase:** `role-job`

## Work map

```yaml
id: waitlist
steps:
  - id: list
    needs: []
    produces: wait
    produce_path: work/waitlist.csv
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/csv-has-columns.py work/waitlist.csv client date
    on_fail: retry
    next: [cal]
  - id: cal
    needs: [wait]
    produces: cal
    produce_path: work/calendar.csv
    tool: docs/tools/calendar.md
    check: python docs/tools/checks/csv-has-columns.py work/calendar.csv date status
    on_fail: retry
    next: [write]
  - id: write
    needs: [wait, cal]
    produces: wait-pack
    produce_path: out/waitlist.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/waitlist.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this shop.
