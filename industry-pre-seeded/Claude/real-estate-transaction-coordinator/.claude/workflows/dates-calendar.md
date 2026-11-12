# Dates Calendar

**When to use:** Build a dates calendar from the executed contract and any executed amendments. Effective date, option or inspection ends, financing, closing, and possession stay on separate rows with the source page. Do not invent typical days. Business versus calendar labels come from their form or broker note; if missing, ask before you count. Holiday moves wait on their holiday file. Appointment times are not silent new legal dates. They watch the clock. You keep the sheet honest and you do not promise a close.

**How to run:** open or select a Work Item under `work-items/<id>/` → follow this file one ready step (or the whole named job if requested) → journal-keeper

**Initial phase:** `role-job`

## Work map

```yaml
id: dates-calendar
steps:
  - id: pull
    needs: []
    produces: contract-dates
    produce_path: work/contract-dates.csv
    tool: docs/tools/contract-pdf.md
    check: python docs/tools/checks/csv-has-columns.py work/contract-dates.csv file effective_date closing_date
    on_fail: retry
    next: [calendar]
  - id: calendar
    needs: [contract-dates]
    produces: calendar
    produce_path: work/dates-calendar.csv
    tool: docs/tools/dates-calendar.md
    check: python docs/tools/checks/file-exists.py work/dates-calendar.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [contract-dates, calendar]
    produces: dates-pack
    produce_path: out/dates-calendar.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/dates-calendar.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this shop.
