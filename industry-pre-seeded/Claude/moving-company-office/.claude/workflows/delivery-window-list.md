# Delivery Window List

**When to use:** List dest windows and spreads from their calendar file and job sheet. Do not invent a clock hour or shrink a spread to look reliable. SIT or dest-TBD rows stay labeled; do not invent a street date. Missing windows on sold deliveries stay questions. They notify customers. You pack the list. Dest-agent names stay as filed, not a promised arrival.

**How to run:** This file is the instruction. After **workflow-selector** records this job:

1. Confirm `work-items/<id>/` exists. Operator calendar and job sheet go in `in/`.
2. For the next ready step, read the named tool under `docs/tools/`.
3. Write the artifact inside the Work Item folder.
4. Run the check from the Work Item folder. Exit 0 = pass. On fail, retry at most 3 times, then ask.
5. **journal-keeper**. One ready step per **continue** unless they asked for the whole job.

**Human gates:** Operator notifies customers. You do not promise a clock hour the file does not show.

**Initial phase:** `role-job` (method phase: dispatch)

## Work map

```yaml
id: delivery-window-list
steps:
  - id: cal
    needs: []
    produces: cal
    produce_path: work/calendar.csv
    tool: docs/tools/calendar-file.md
    check: python docs/tools/checks/csv-has-columns.py work/calendar.csv job date
    on_fail: retry
    next: [jobs]
  - id: jobs
    needs: [cal]
    produces: jobs
    produce_path: work/jobs.csv
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/csv-has-columns.py work/jobs.csv job date
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [cal, jobs]
    produces: window-pack
    produce_path: out/delivery-windows.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/delivery-windows.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator confirms how *this* shop files.
