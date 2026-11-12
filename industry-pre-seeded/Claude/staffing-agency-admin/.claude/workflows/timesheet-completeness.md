# Timesheet Completeness

**When to use:** For the period they named, join assignments that should have hours to the timesheet CSV. List missing files, missing punches, blank totals, and missing client-sign or approval ticks. Do not invent hours. Do not approve. Do not decide overtime as law. If punches and signed totals disagree, quote both and ask. Write the completeness list and a pack. They chase the site. No portal password and no SSN in docs/.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put timesheet CSV and assignments in `in/`. Read this file and the named `docs/tools/` doc. Walk one ready YAML step (or the whole job if requested): produce the file under this Work Item’s `work/` or `out/`, run the check, then journal-keeper. Do not skip a step with a chat summary.

**Initial phase:** `role-job`

## Work map

```yaml
id: timesheet-completeness
steps:
  - id: ts
    needs: []
    produces: timesheets
    produce_path: work/timesheets.csv
    tool: docs/tools/timesheet-csv.md
    check: python docs/tools/checks/csv-has-columns.py work/timesheets.csv name hours
    on_fail: retry
    next: [assign]
  - id: assign
    needs: [timesheets]
    produces: assign
    produce_path: work/assignments.csv
    tool: docs/tools/assignment-sheet.md
    check: python docs/tools/checks/file-exists.py work/assignments.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [timesheets, assign]
    produces: ts-pack
    produce_path: out/timesheet-completeness.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/timesheet-completeness.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this shop.
