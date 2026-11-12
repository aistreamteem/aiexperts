# Truck Load

**When to use:** Jobs on one tech or crew, combined packing list, missing special orders. They load the truck. Pull the day's jobs for the name they gave, then merge SKUs and qty. Compare to truck stock; do not invent on-hand. Will-call parts need job ids so nothing sits unassigned. Tool or recovery lines appear only if their template includes them. Weather holds and two-person flags stay visible. The write-up lists missing specials as questions. You do not drive the route.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put source files in `in/`. Walk one ready YAML step (or the whole named job if requested): produce the file, run the check, then **journal-keeper**.

**Initial phase:** `role-job`

## Work map

```yaml
id: truck-load
steps:
  - id: day-jobs
    needs: []
    produces: load-jobs
    produce_path: work/load-jobs.csv
    tool: docs/tools/schedule-sheet.md
    check: python docs/tools/checks/file-exists.py work/load-jobs.csv
    on_fail: retry
    next: [combined]
  - id: combined
    needs: [load-jobs]
    produces: load-list
    produce_path: work/load-packing.csv
    tool: docs/tools/packing-list-sheet.md
    check: python docs/tools/checks/csv-has-columns.py work/load-packing.csv sku qty
    on_fail: retry
    next: [missing]
  - id: missing
    needs: [load-list]
    produces: load-missing
    produce_path: out/truck-load.md
    tool: docs/tools/truck-stock.md
    check: python docs/tools/checks/file-exists.py out/truck-load.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this shop (**remember**).
