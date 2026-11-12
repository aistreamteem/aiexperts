# Warranty Parts

**When to use:** One job they name: serial, install date, failed part from their file, order question. No manufacturer promise. Do not invent a start date or swap a serial. Do not register as the maker. Quote plate photo, invoice, and packing list when they disagree. Labor versus parts clocks stay separate. Core or RMA tags follow their steps; do not promise a credit. The pack lists the order ask for the house without paying. Missing serial is a question. Their register columns win.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put source files in `in/`. Walk one ready YAML step (or the whole named job if requested): produce the file, run the check, then **journal-keeper**.

**Initial phase:** `role-job`

## Work map

```yaml
id: warranty-parts
steps:
  - id: job
    needs: []
    produces: warranty-job
    produce_path: work/warranty-job.csv
    tool: docs/tools/warranty-file.md
    check: python docs/tools/checks/file-exists.py work/warranty-job.csv
    on_fail: retry
    next: [serial]
  - id: serial
    needs: [warranty-job]
    produces: warranty-serial
    produce_path: work/warranty-serial.csv
    tool: docs/tools/warranty-file.md
    check: python docs/tools/checks/csv-has-columns.py work/warranty-serial.csv job serial
    on_fail: retry
    next: [order-ask]
  - id: order-ask
    needs: [warranty-serial]
    produces: warranty-pack
    produce_path: out/warranty-parts.md
    tool: docs/tools/parts-vendor.md
    check: python docs/tools/checks/file-exists.py out/warranty-parts.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this shop (**remember**).
