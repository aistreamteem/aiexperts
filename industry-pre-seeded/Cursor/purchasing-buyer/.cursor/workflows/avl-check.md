# AVL Check

**When to use:** Check each proposed vendor on the requisition or draft against the approved-vendor list they exported. Not on the list: ask. Do not add the vendor as approved and do not treat a one-time or sole-source note as an AVL add. If they have no AVL, say so. Inactive or conditional status stays as written. The pack is a pass/fail list plus questions, not a live PO. They add names if they choose. Then they approve any later PO.

**How to run:** Select this job with workflow-selector (or continue). Use `work-items/<id>/`. Put source files in `in/`. Walk one ready step: read the named tool doc, write the produced file under this Work Item, run the check, then journal-keeper. Do not skip a step with a chat summary. Whole named job only if they asked.

**Initial phase:** `role-job`

## Work map

```yaml
id: avl-check
steps:
  - id: avl
    needs: []
    produces: avl
    produce_path: work/avl.csv
    tool: docs/tools/avl-sheet.md
    check: python docs/tools/checks/csv-has-columns.py work/avl.csv vendor
    on_fail: retry
    next: [req]
  - id: req
    needs: [avl]
    produces: req
    produce_path: work/requisitions.csv
    tool: docs/tools/requisition-sheet.md
    check: python docs/tools/checks/file-exists.py work/requisitions.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [avl, req]
    produces: avl-pack
    produce_path: out/avl-check.md
    tool: docs/tools/avl-sheet.md
    check: python docs/tools/checks/file-exists.py out/avl-check.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they confirm how *this* shop files and checks the pack.
