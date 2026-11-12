# Parts order versus estimate

**When to use:** Join the parts PO sheet to estimate lines: part, qty, source, promised date, backorder. Do not invent a price or an ETA. Extras on the PO that are not on the estimate stay listed. Returns stay listed. You do not pay the vendor. Write-up is the match plus holes, not a substitute you pick and not a silent estimate edit.

**How to run:** Confirm the Work Item under `work-items/<id>/`. Walk the YAML steps in this file via **continue** (one ready step, or the whole named job if requested). Read the cited `docs/tools/` file, write artifacts under this Work Item's `work/` and `out/`, run the step `check` against those paths, then **journal-keeper**.

**Initial phase:** first YAML step in this file

## Work map

```yaml
id: parts-order-vs-estimate
steps:
  - id: po
    needs: []
    produces: po
    produce_path: work/parts-po.csv
    tool: docs/tools/parts-po-sheet.md
    check: python docs/tools/checks/csv-has-columns.py work/parts-po.csv part qty
    on_fail: retry
    next: [est]
  - id: est
    needs: [po]
    produces: est
    produce_path: work/estimate-lines.csv
    tool: docs/tools/estimate-export.md
    check: python docs/tools/checks/file-exists.py work/estimate-lines.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [po, est]
    produces: po-pack
    produce_path: out/parts-order-vs-estimate.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/parts-order-vs-estimate.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects this shop's process (**remember**).
