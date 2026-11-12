# Emergency and after-hours list

**When to use:** List tickets they coded emergency or after-hours, then attach the after-hours vendor or on-call names from their contractor list and any silent-hours or holiday notes on the plant calendar. Do not invent a vendor. Do not store alarm codes. Do not promote a routine ticket. Write-up is a morning recap pack: who is down, who is on the list, and which calendar window applies, not a diagnosis.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put source files in `in/`. Walk one ready YAML step (or the whole named job if requested): produce the file, run the check, then **journal-keeper**. Paths `in/`, `work/`, `out/`, and `evidence/` are inside that Work Item.

**Initial phase:** `role-job`

## Work map

```yaml
id: emergency-after-hours-list
steps:
  - id: tickets
    needs: []
    produces: tickets
    produce_path: work/wo.csv
    tool: docs/tools/wo-csv.md
    check: python docs/tools/checks/csv-has-columns.py work/wo.csv wo asset priority
    on_fail: retry
    next: [vendors]
  - id: vendors
    needs: [tickets]
    produces: vendors
    produce_path: work/after-hours-vendors.csv
    tool: docs/tools/contractor-list.md
    check: python docs/tools/checks/file-exists.py work/after-hours-vendors.csv
    on_fail: retry
    next: [cal]
  - id: cal
    needs: [tickets, vendors]
    produces: cal
    produce_path: work/calendar.csv
    tool: docs/tools/calendar.md
    check: python docs/tools/checks/file-exists.py work/calendar.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [tickets, vendors, cal]
    produces: emergency-pack
    produce_path: out/emergency-after-hours.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/emergency-after-hours.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects this plant through **remember**.
