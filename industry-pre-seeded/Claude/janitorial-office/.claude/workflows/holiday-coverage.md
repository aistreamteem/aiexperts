# Holiday Coverage

**When to use:** Read their holiday calendar against the schedule and roster. List sites that skip, sites that still run, and extra-day rows that already have auth. Do not invent a federal skip or a party night. Quote company versus customer calendar conflicts. Crew names come from the roster only. Write-up is coverage holes plus questions. They call the customer. You do not declare the building closed.

**How to run:** Use **continue** with this workflow. Work inside `work-items/<id>/`. For each step: read the tool doc, produce the file, run the check (retry at most 3, then ask), then **journal-keeper**. Do not invent a federal skip or a party night.

**Initial phase:** `cal`

## Work map

```yaml
id: holiday-coverage
steps:
  - id: cal
    needs: []
    produces: calendar
    produce_path: work/holiday-calendar.csv
    tool: docs/tools/calendar.md
    check: python docs/tools/checks/file-exists.py work/holiday-calendar.csv
    on_fail: retry
    next: [schedule]
  - id: schedule
    needs: [calendar]
    produces: schedule
    produce_path: work/holiday-schedule.csv
    tool: docs/tools/schedule-csv.md
    check: python docs/tools/checks/file-exists.py work/holiday-schedule.csv
    on_fail: retry
    next: [roster]
  - id: roster
    needs: [schedule]
    produces: roster
    produce_path: work/holiday-roster.csv
    tool: docs/tools/crew-roster.md
    check: python docs/tools/checks/file-exists.py work/holiday-roster.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [calendar, schedule, roster]
    produces: holiday-pack
    produce_path: out/holiday-coverage.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/holiday-coverage.md
    on_fail: retry
    next: []
```

Starter map. Replace tools and checks when the operator corrects this shop (**remember**).
