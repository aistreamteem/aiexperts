# Receiving Shorts

**When to use:** From receiving versus open PO quantity, list shorts and partials in those words. Do not write received-in-full. Attach packing-slip notes or photos if they scanned them, and list slip qty when it differs from the dock count. Remaining open qty stays visible. One vendor per rush pack unless they asked otherwise. You do not invent a count and you do not zero the remainder. They send the claim to the vendor.

**How to run:** Select this job with workflow-selector (or continue). Use `work-items/<id>/`. Put source files in `in/`. Walk one ready step: read the named tool doc, write the produced file under this Work Item, run the check, then journal-keeper. Do not skip a step with a chat summary. Whole named job only if they asked.

**Initial phase:** `role-job`

## Work map

```yaml
id: receiving-shorts
steps:
  - id: recv
    needs: []
    produces: recv
    produce_path: work/receiving.csv
    tool: docs/tools/receiving.md
    check: python docs/tools/checks/csv-has-columns.py work/receiving.csv po sku qty
    on_fail: retry
    next: [slip]
  - id: slip
    needs: [recv]
    produces: slip
    produce_path: work/packing-slips.csv
    tool: docs/tools/packing-slip-folder.md
    check: python docs/tools/checks/file-exists.py work/packing-slips.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [recv, slip]
    produces: short-pack
    produce_path: out/shorts.md
    tool: docs/tools/receiving.md
    check: python docs/tools/checks/file-exists.py out/shorts.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they confirm how *this* shop files and checks the pack.
