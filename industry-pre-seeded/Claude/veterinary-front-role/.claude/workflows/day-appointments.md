# Day Appointments

**When to use:** List from export. Flag emergency wording at the top. No clinical commentary. One date. Confirm the export timestamp and the site name before you treat the file as today's book. Keep reason text as typed. Keep doctor versus technician columns as labeled. Do not mix two dates or two hospitals. Do not shorten types to fill holes. Write the huddle list and the pack from the same rows. Starter / guess until they teach type lengths and interrupt rules.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put the appointment export in `in/`. Read this file and `docs/tools/pims-export.md`. Walk one ready YAML step (or the whole job if requested): produce the file under this Work Item’s `work/` or `out/`, run the check, then journal-keeper. Do not skip a step with a chat summary.

**Initial phase:** `role-job`

## Work map

```yaml
id: day-appointments
steps:
  - id: pull
    needs: []
    produces: appt
    produce_path: work/appointments.csv
    tool: docs/tools/pims-export.md
    check: python docs/tools/checks/file-exists.py work/appointments.csv
    on_fail: retry
    next: [columns]
  - id: columns
    needs: [appt]
    produces: appt-cols
    produce_path: work/appointments.csv
    tool: docs/tools/pims-export.md
    check: python docs/tools/checks/csv-has-columns.py work/appointments.csv time patient
    on_fail: retry
    next: [write]
  - id: write
    needs: [appt-cols]
    produces: appt-writeup
    produce_path: out/appointments.md
    tool: docs/tools/pims-export.md
    check: python docs/tools/checks/file-exists.py out/appointments.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this clinic.
