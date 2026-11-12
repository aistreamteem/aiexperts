# Order Guide

**When to use:** Build an order CSV from counted on-hand versus their par for one vendor and one delivery date. No guessed on-hand: if the count file is missing or a row is blank, ask or leave qty empty with a question. Do not invent a par, case pack, or filler SKU to hit a minimum. Label splits and one-time or catering lines so they do not become a silent standing par. The pack lists open questions; they place the order in the portal. Starter columns are orientation until they confirm this guide.

**How to run:** Self-contained. Active Work Item under `work-items/<id>/`. For each ready step: read the tool doc → write `produce_path` inside that Work Item → run the check with working directory = the Work Item folder → journal-keeper. One **continue** = one ready step unless they asked to finish this job. Missing count, par, on-hand, or allergen pointers are a human gate, not a number you fill.

**Initial phase:** `count`

## Work map

```yaml
id: order-guide
steps:
  - id: count
    needs: []
    produces: count
    produce_path: work/count.csv
    tool: docs/tools/count-sheet.md
    check: python docs/tools/checks/csv-has-columns.py work/count.csv item qty
    on_fail: retry
    next: [order]
  - id: order
    needs: [count]
    produces: order
    produce_path: work/order.csv
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/csv-has-columns.py work/order.csv item qty
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [order]
    produces: order-pack
    produce_path: out/order.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/order.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator confirms how this kitchen files (`remember` / `integrate-docs`).
