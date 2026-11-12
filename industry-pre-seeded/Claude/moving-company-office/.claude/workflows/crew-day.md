# Crew Day

**When to use:** Build the day list from their roster plus the calendar jobs they already booked. Copy planned headcount; do not invent a person or a wage. Canceled rows they marked stay off the live list. Piano, safe, or hoist notes stay attached as they wrote them. Gate codes stay out of the pack. They dispatch. You write the list. Overtime hours are not invented.

**How to run:** This file is the instruction. After **workflow-selector** records this job:

1. Confirm `work-items/<id>/` exists. Operator roster and calendar go in `in/`.
2. For the next ready step, read the named tool under `docs/tools/`.
3. Write the artifact inside the Work Item folder.
4. Run the check from the Work Item folder. Exit 0 = pass. On fail, retry at most 3 times, then ask.
5. **journal-keeper**. One ready step per **continue** unless they asked for the whole job.

**Human gates:** Operator dispatches. Missing roster → ask. Do not fill a call-out with a guessed helper. Do not pay the crew.

**Initial phase:** `role-job` (method phase: dispatch)

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

Starter work map. Replace tools and checks when the operator confirms how *this* shop files.
