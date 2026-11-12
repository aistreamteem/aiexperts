# Class roster

**When to use:** Build the roster for named classes from the schedule file plus check-ins or bookings they exported. Capacity comes only from the schedule. Do not overbook unless their file allows it. Waitlist rows stay off the booked count. Holiday hours beat a leftover series class. Produce the roster plus a pack note. They teach the class. Starter until they teach this studio’s live schedule file.

**How to run:** Open or continue the Work Item under `work-items/<id>/`. Follow this file's YAML via **continue**. Read the cited `docs/tools/` doc, write artifacts under the Work Item, run the step `check`, store logs in `evidence/`, then **journal-keeper**.

**Initial phase:** `role-job`

## Work map

```yaml
id: class-roster
steps:
  - id: schedule
    needs: []
    produces: schedule
    produce_path: work/class-schedule.csv
    tool: docs/tools/class-schedule.md
    check: python docs/tools/checks/csv-has-columns.py work/class-schedule.csv class_id start
    on_fail: retry
    next: [hours]
  - id: hours
    needs: [schedule]
    produces: hours
    produce_path: work/holiday-hours.csv
    tool: docs/tools/holiday-hours.md
    check: python docs/tools/checks/file-exists.py work/holiday-hours.csv
    on_fail: retry
    next: [checkins]
  - id: checkins
    needs: [hours]
    produces: checkins
    produce_path: work/class-check-in.csv
    tool: docs/tools/check-in-csv.md
    check: python docs/tools/checks/file-exists.py work/class-check-in.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [schedule, hours, checkins]
    produces: roster-pack
    produce_path: out/class-roster.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/class-roster.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects this shop.
