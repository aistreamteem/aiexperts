# RFQ From Files

**When to use:** Assemble the item list, quantities, specs or drawings they attached, and need-by from their requisition files. Tabulate quotes only when PDFs arrive in the quote folder; blank cells stay blank. They send the RFQ and they award. You do not pick a winner and you do not email vendors as this product. Same package to each invited vendor if that is their rule. AVL still applies to invitees when they use one. Expired incoming quotes stay labeled expired.

**How to run:** Select this job with workflow-selector (or continue). Use `work-items/<id>/`. Put source files in `in/`. Walk one ready step: read the named tool doc, write the produced file under this Work Item, run the check, then journal-keeper. Do not skip a step with a chat summary. Whole named job only if they asked.

**Initial phase:** `role-job`

## Work map

```yaml
id: rfq-from-files
steps:
  - id: req
    needs: []
    produces: req
    produce_path: work/rfq-items.csv
    tool: docs/tools/requisition-sheet.md
    check: python docs/tools/checks/csv-has-columns.py work/rfq-items.csv sku qty
    on_fail: retry
    next: [folder]
  - id: folder
    needs: [req]
    produces: quotes
    produce_path: work/quote-folder.csv
    tool: docs/tools/quote-folder.md
    check: python docs/tools/checks/file-exists.py work/quote-folder.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [req, quotes]
    produces: rfq-pack
    produce_path: out/rfq.md
    tool: docs/tools/quote-folder.md
    check: python docs/tools/checks/file-exists.py out/rfq.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they confirm how *this* shop files and checks the pack.
