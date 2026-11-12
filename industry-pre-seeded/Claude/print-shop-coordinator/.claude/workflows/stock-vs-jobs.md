# Stock Vs Jobs

**When to use:** Compare on-hand stock to the pull implied by open tickets. Shortages stay visible. Do not substitute a close sheet. Do not count CFS as mill on-hand unless they receipted it that way. Special-order rows stay special. You do not invent a sheet count and you do not pay a mill. The pack is a shortage list plus which tickets wait on paper.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put source files in `in/`. Walk one ready YAML step (or the whole named job if requested): produce the file, run the check, then **journal-keeper**.

**Initial phase:** isolate / intake

## Work map

```yaml
id: stock-vs-jobs
steps:
  - id: stock
    needs: []
    produces: stock
    produce_path: work/stock.csv
    tool: docs/tools/stock-csv.md
    check: python docs/tools/checks/csv-has-columns.py work/stock.csv item qty
    on_fail: retry
    next: [tickets]
  - id: tickets
    needs: [stock]
    produces: tickets
    produce_path: work/job-tickets.csv
    tool: docs/tools/job-ticket-sheet.md
    check: python docs/tools/checks/file-exists.py work/job-tickets.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [stock, tickets]
    produces: stock-pack
    produce_path: out/stock-vs-jobs.md
    tool: docs/tools/stock-csv.md
    check: python docs/tools/checks/file-exists.py out/stock-vs-jobs.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they **remember** a correction for this shop.
