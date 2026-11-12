# Redo Log

**When to use:** From their order sheet or redo workbook, list remake rows: original job, new job if assigned, and their reason code. Do not invent lab-error or non-adapt. Do not interpret the old or new Rx. Blank reason stays a question; do not treat the redo as complete. Warranty versus billable comes only from their warranty wording they already stored plus that code. Produce the log plus a pack note. Prefer job numbers. Extra complaint narrative stays out of docs/ when the code exists.

**How to run:** Select this job with **workflow-selector** (or name it). Keep artifacts under `work-items/<id>/`. Walk one ready step per **continue** unless they asked for the whole job. For each step: read the tool file, write `produce_path` inside the Work Item folder, run the check against that same path, store the log in `evidence/`, then **journal-keeper**. Do not start a step if its `needs` files are missing. On check fail, retry at most 3 times, then ask. If a required export is missing, ask; do not invent rows.

**Initial phase:** `intake`, then the first YAML step. Paths `work/` and `out/` mean inside the current Work Item.

## Work map

```yaml
id: redo-log
steps:
  - id: redos
    needs: []
    produces: redos
    produce_path: work/redo-log.csv
    tool: docs/tools/frame-order-sheet.md
    check: python docs/tools/checks/file-exists.py work/redo-log.csv
    on_fail: retry
    next: [columns]
  - id: columns
    needs: [redos]
    produces: redo-cols
    produce_path: work/redo-log.csv
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/csv-has-columns.py work/redo-log.csv job reason
    on_fail: retry
    next: [write]
  - id: write
    needs: [redo-cols]
    produces: redo-writeup
    produce_path: out/redo-log.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/redo-log.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this office via **remember**.
