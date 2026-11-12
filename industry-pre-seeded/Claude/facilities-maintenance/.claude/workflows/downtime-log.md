# Downtime log pack

**When to use:** Build a downtime pack from their downtime log: asset, start, end if any, duration as they stored it, and downtime code from their list. Do not invent an end. Do not hide an open outage. Do not pick a code from a work-order sentence. Write-up quotes the log and flags tickets that look down with no row, or rows with no matching work order, as questions rather than a production-scheduler rewrite.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put source files in `in/`. Walk one ready YAML step (or the whole named job if requested): produce the file, run the check, then **journal-keeper**. Paths `in/`, `work/`, `out/`, and `evidence/` are inside that Work Item.

**Initial phase:** `role-job`

## Work map

```yaml
id: downtime-log
steps:
  - id: log
    needs: []
    produces: log
    produce_path: work/downtime.csv
    tool: docs/tools/downtime-log.md
    check: python docs/tools/checks/csv-has-columns.py work/downtime.csv asset start code
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [log]
    produces: downtime-pack
    produce_path: out/downtime-log.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/downtime-log.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects this plant through **remember**.
