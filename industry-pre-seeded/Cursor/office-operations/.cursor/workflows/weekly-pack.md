# Weekly Pack

**When to use:** From their task sheet and calendar export, list this week's items and missing files. One week unless they asked to combine. Confirm week start if the export and wall calendar disagree. Do not add meetings they did not export. Conflicts: list both and ask. Owners stay as they wrote; blank owner is a question, not a name you pick. Draft the write-up as a file; they send anything to people. Starter notes, not this shop's proven ritual until they teach.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put source files in `in/`. Walk one ready YAML step (or the whole named job if requested): read the named tool doc, produce the file, run the check, then **journal-keeper**.

**Initial phase:** `role-job`

## Work map

```yaml
id: weekly-pack
steps:
  - id: pull
    needs: []
    produces: week-raw
    produce_path: work/week-raw.csv
    tool: docs/tools/calendar-export.md
    check: python docs/tools/checks/csv-has-columns.py work/week-raw.csv date title
    on_fail: retry
    next: [tasks]
  - id: tasks
    needs: [week-raw]
    produces: week-tasks
    produce_path: work/week-tasks.csv
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/csv-has-columns.py work/week-tasks.csv task owner
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [week-tasks]
    produces: week-pack
    produce_path: out/weekly-office.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/weekly-office.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this shop.
