# Crew day list

**When to use:** Build the day list from their roster plus the calendar jobs they already booked. Copy planned headcount; do not invent a person or a wage. Canceled rows they marked stay off the live list. Piano, safe, or hoist notes stay attached as they wrote them. Gate codes stay out of the pack. They dispatch. You write the list and a short pack note. Overtime hours are not invented.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put source files in `in/`. Walk one ready YAML step (or the whole named job if requested): read the named tool, produce the file, run the check, then **journal-keeper**. Do not invent weight, cube, rates, crew names, or delivery hours.

**Initial phase:** `role-job`

## Work map

```yaml
id: crew-day
steps:
  - id: roster
    needs: []
    produces: roster
    produce_path: work/crew-roster.csv
    tool: docs/tools/crew-roster.md
    check: python docs/tools/checks/csv-has-columns.py work/crew-roster.csv crew name
    on_fail: retry
    next: [cal]
  - id: cal
    needs: [roster]
    produces: cal
    produce_path: work/calendar.csv
    tool: docs/tools/calendar-file.md
    check: python docs/tools/checks/csv-has-columns.py work/calendar.csv job date
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [roster, cal]
    produces: crew-day-pack
    produce_path: out/crew-day.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/crew-day.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects this shop.
