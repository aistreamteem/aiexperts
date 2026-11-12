# Retail Count

**When to use:** From their count sheet, list on-hand, flag SKUs below par if the sheet has par, and keep retail off the backbar column. Reorder quantities come from the vendor PDF, not a guess. Match SKU and size. Do not place the order or pay the house account. A backbar empty is not a retail sale. If par or case pack is missing, say so and ask. They send the vendor order. Starter until they teach this shop’s bins and vendors.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put source files in that item’s `in/`. Walk one ready YAML step (or the whole named job if requested): produce the file, run the check, then **journal-keeper**. Paths `in/`, `work/`, `out/`, and `evidence/` are inside that Work Item.

**Initial phase:** `role-job`

## Work map

```yaml
id: retail-count
steps:
  - id: count
    needs: []
    produces: retail
    produce_path: work/retail-count.csv
    tool: docs/tools/retail-sheet.md
    check: python docs/tools/checks/csv-has-columns.py work/retail-count.csv sku on_hand
    on_fail: retry
    next: [vendor]
  - id: vendor
    needs: [retail]
    produces: vendor
    produce_path: work/vendor-retail.pdf
    tool: docs/tools/vendor-retail-pdf.md
    check: python docs/tools/checks/file-exists.py work/vendor-retail.pdf
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [retail, vendor]
    produces: retail-pack
    produce_path: out/retail-count.md
    tool: docs/tools/retail-sheet.md
    check: python docs/tools/checks/file-exists.py out/retail-count.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects this shop (**remember**).
