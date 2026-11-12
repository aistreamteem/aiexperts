# Missing Rx On Order

**When to use:** From the frame-order sheet, list jobs that their process says need a spectacle or contact-lens Rx file and the file is not present. Do not interpret a Rx image to finish the ticket. Do not invent PD, add, or lens type. Do not mark the ticket complete. Outside-Rx transfers still need a named file. Produce the missing-Rx list plus a pack note. They obtain the file. Prefer chart and job number. Extra refraction values stay out of docs/ when a present-or-missing flag will do.

**How to run:** Select this job with **workflow-selector** (or name it). Keep artifacts under `work-items/<id>/`. Walk one ready step per **continue** unless they asked for the whole job. For each step: read the tool file, write `produce_path` inside the Work Item folder, run the check against that same path, store the log in `evidence/`, then **journal-keeper**. Do not start a step if its `needs` files are missing. On check fail, retry at most 3 times, then ask. If a required export is missing, ask; do not invent rows.

**Initial phase:** `intake`, then the first YAML step. Paths `work/` and `out/` mean inside the current Work Item.

## Work map

```yaml
id: missing-rx-on-order
steps:
  - id: orders
    needs: []
    produces: orders
    produce_path: work/frame-orders.csv
    tool: docs/tools/frame-order-sheet.md
    check: python docs/tools/checks/file-exists.py work/frame-orders.csv
    on_fail: retry
    next: [columns]
  - id: columns
    needs: [orders]
    produces: order-cols
    produce_path: work/frame-orders.csv
    tool: docs/tools/frame-order-sheet.md
    check: python docs/tools/checks/csv-has-columns.py work/frame-orders.csv chart job
    on_fail: retry
    next: [write]
  - id: write
    needs: [order-cols]
    produces: rx-writeup
    produce_path: out/missing-rx.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/missing-rx.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this office via **remember**.
