# Recert dates

**When to use:** From their recert or POC tracker and the referral folder, list recert due dates and POC end dates as stored. Do not invent a ninety-day interval as a Medicare opinion. Do not write the recert note. Missing dates stay questions. Prefer chart label and therapist if present. Flag booked visits that their file places after a POC end date. Produce the date list plus a write-up. They obtain signatures. You pack completeness.

**How to run:** Open or reuse `work-items/<id>/`. Put source files in `in/`. Follow this map in order: read the named `docs/tools/` file, write `produce_path` inside this Work Item, run the step `check`, retry at most 3 times on fail then ask. Pass produced files to the next step. One ready step per continue unless the operator asked for the whole job. Then journal-keeper.

**Initial phase:** `role-job`

## Work map

```yaml
id: recert-dates
steps:
  - id: dates
    needs: []
    produces: recert
    produce_path: work/recert-dates.csv
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/csv-has-columns.py work/recert-dates.csv chart due
    on_fail: retry
    next: [poc]
  - id: poc
    needs: [recert]
    produces: poc
    produce_path: work/poc-index.csv
    tool: docs/tools/referral-folder.md
    check: python docs/tools/checks/file-exists.py work/poc-index.csv
    on_fail: retry
    next: [write]
  - id: write
    needs: [recert, poc]
    produces: recert-writeup
    produce_path: out/recert-dates.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/recert-dates.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator confirms how this clinic works.
