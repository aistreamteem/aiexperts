# Change Order Pack

**When to use:** Show the original PO line versus the requested change (quantity, date, price, revision, or ship-to) with the vendor PDF or buyer note that triggered it. They approve. Do not silently edit the open-PO sheet so aging looks right. An acknowledgment that changes terms is a change, not the word confirmed. Old versus new must both appear. You do not send the change as live. Closing short is a separate decision they make in words.

**How to run:** Select this job with workflow-selector (or continue). Use `work-items/<id>/`. Put source files in `in/`. Walk one ready step: read the named tool doc, write the produced file under this Work Item, run the check, then journal-keeper. Do not skip a step with a chat summary. Whole named job only if they asked.

**Initial phase:** `role-job`

## Work map

```yaml
id: change-order-pack
steps:
  - id: pos
    needs: []
    produces: pos
    produce_path: work/pos.csv
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py work/pos.csv
    on_fail: retry
    next: [change]
  - id: change
    needs: [pos]
    produces: change
    produce_path: work/change-request.csv
    tool: docs/tools/vendor-pdf.md
    check: python docs/tools/checks/file-exists.py work/change-request.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [pos, change]
    produces: co-pack
    produce_path: out/change-order.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/change-order.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they confirm how *this* shop files and checks the pack.
