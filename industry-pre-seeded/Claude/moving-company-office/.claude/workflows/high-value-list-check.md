# High Value List Check

**When to use:** Check whether their high-value form is present when their rule or estimate PDF says it is required. List blank description or value fields they left open. Do not invent an article or a dollar. Valuation on the main form is not a substitute if they split the papers. They collect the list. You write present-or-missing. Claims still route; you do not decide coverage.

**How to run:** This file is the instruction. After **workflow-selector** records this job:

1. Confirm `work-items/<id>/` exists. Operator inventory and estimate PDF go in `in/`.
2. For the next ready step, read the named tool under `docs/tools/`.
3. Write the artifact inside the Work Item folder.
4. Run the check from the Work Item folder. Exit 0 = pass. On fail, retry at most 3 times, then ask.
5. **journal-keeper**. One ready step per **continue** unless they asked for the whole job.

**Human gates:** Operator collects the high-value list. You do not invent items or values.

**Initial phase:** `role-job` (method phase: inventory)

## Work map

```yaml
id: high-value-list-check
steps:
  - id: inv
    needs: []
    produces: inv
    produce_path: work/inventory.csv
    tool: docs/tools/inventory-sheet.md
    check: python docs/tools/checks/csv-has-columns.py work/inventory.csv job item qty
    on_fail: retry
    next: [est]
  - id: est
    needs: [inv]
    produces: est
    produce_path: work/estimate.pdf
    tool: docs/tools/estimate-pdf.md
    check: python docs/tools/checks/file-exists.py work/estimate.pdf
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [inv, est]
    produces: hvl-pack
    produce_path: out/high-value-check.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/high-value-check.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator confirms how *this* shop files.
