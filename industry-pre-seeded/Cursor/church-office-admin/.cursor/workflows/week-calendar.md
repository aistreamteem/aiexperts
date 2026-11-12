# Week calendar pack

**When to use:** Build the week's room and building pack from their calendar file. Copy room, date, start, and who they named. Flag collisions and blank rooms on events they already accepted. Do not invent a hold. Do not free a Saturday because it looks open. Weddings, funerals, and outside use stay on the rows they stored. Write-up names which file won when two calendars disagree. They publish. You pack the week.

**How to run:** Open or continue the Work Item under `work-items/<id>/`. Walk one ready YAML step (or the whole named job if requested): produce the file, run the check, then journal-keeper.

**Initial phase:** `role-job`

## Work map

```yaml
id: week-calendar
steps:
  - id: pull
    needs: []
    produces: calendar
    produce_path: work/week-calendar.csv
    tool: docs/tools/calendar.md
    check: python docs/tools/checks/csv-has-columns.py work/week-calendar.csv date room
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [calendar]
    produces: week-pack
    produce_path: out/week-calendar.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/week-calendar.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this shop (**remember**).
