# Quote Lead MOQ

**When to use:** Read the quote PDFs they saved. List unit price, currency as labeled, validity date, MOQ or pack, and lead time as written. Blank fields stay blank and become asks. No guessed prices, breaks, or freight dollars. If the quote is expired, ask before anyone uses the price. Compare to the item master when that export exists; if they disagree, quote both. They decide reuse, a new quote, or a substitute. You do not issue a PO from this pack alone.

**How to run:** Select this job with workflow-selector (or continue). Use `work-items/<id>/`. Put source files in `in/`. Walk one ready step: read the named tool doc, write the produced file under this Work Item, run the check, then journal-keeper. Do not skip a step with a chat summary. Whole named job only if they asked.

**Initial phase:** `role-job`

## Work map

```yaml
id: quote-lead-moq
steps:
  - id: pdf
    needs: []
    produces: quotes
    produce_path: work/quotes.csv
    tool: docs/tools/vendor-pdf.md
    check: python docs/tools/checks/file-exists.py work/quotes.csv
    on_fail: retry
    next: [items]
  - id: items
    needs: [quotes]
    produces: items
    produce_path: work/item-master.csv
    tool: docs/tools/item-master-csv.md
    check: python docs/tools/checks/file-exists.py work/item-master.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [quotes, items]
    produces: quote-pack
    produce_path: out/quote-lead-moq.md
    tool: docs/tools/vendor-pdf.md
    check: python docs/tools/checks/file-exists.py out/quote-lead-moq.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they confirm how *this* shop files and checks the pack.
