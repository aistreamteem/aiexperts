# Week calendar pack

**When to use:** Build the week's room and building pack from their calendar file. Copy room, date, start, and who they named. Flag collisions and blank rooms on events they already accepted. Do not invent a hold. Do not free a Saturday because it looks open. Weddings, funerals, and outside use stay on the rows they stored. Write-up names which file won when two calendars disagree. They publish. You pack the week.

**How to run:** Open `work-items/<id>/`. Read this file. For one ready step (or the whole job if they asked): follow the `tool` doc, write `produce_path` inside that Work Item, run `check` from there. Then journal-keeper. See `.claude/workflows/README.md`.

**Initial phase:** `intake`

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

Starter work map. Replace tools and checks when the operator corrects how this office works.
