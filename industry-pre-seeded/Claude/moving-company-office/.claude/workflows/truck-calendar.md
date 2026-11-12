# Truck Calendar

**When to use:** List unit, date, and job from their truck calendar. Flag two firsts on one truck and jobs with no unit. Do not invent a free day or an empty weight. Shuttle units stay labeled if they coded them. Hired-hauler rows stay as they wrote them. They dispatch. You pack collisions and questions. Scale tickets are a different pack; do not fill tare from hope on this list.

**How to run:** This file is the instruction. After **workflow-selector** records this job:

1. Confirm `work-items/<id>/` exists. Operator truck calendar and job sheet go in `in/`.
2. For the next ready step, read the named tool under `docs/tools/`.
3. Write the artifact inside the Work Item folder.
4. Run the check from the Work Item folder. Exit 0 = pass. On fail, retry at most 3 times, then ask.
5. **journal-keeper**. One ready step per **continue** unless they asked for the whole job.

**Human gates:** Operator books or moves jobs. You flag collisions; you do not invent a free day.

**Initial phase:** `role-job` (method phase: dispatch)

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

Starter work map. Replace tools and checks when the operator confirms how *this* shop files.
