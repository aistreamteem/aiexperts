# Receiving match

**When to use:** Match purchase order versus packing slip versus dock count. Flag shorts, overs, damage, extra lines, UOM mismatches, and missing tickets. No invented PO. ASN is a plan, not a receipt. BOL is not a line count and not a customs clearance. Keep lot or serial if the master requires them. You do not hide a short, mark received in full, or send money. Quote the PDFs and CSVs you used and say which file was absent.

**How to run:** Open or switch to a Work Item under `work-items/<id>/`. Follow this YAML one ready step (or the whole named job if requested). Then **journal-keeper**.

**Initial phase:** `role-job`

## Work map

```yaml
id: receiving-match
steps:
  - id: po
    needs: []
    produces: po-raw
    produce_path: work/open-po.csv
    tool: docs/tools/po-pdf.md
    check: python docs/tools/checks/csv-has-columns.py work/open-po.csv po sku qty
    on_fail: retry
    next: [dock]
  - id: dock
    needs: [po-raw]
    produces: recv-raw
    produce_path: work/receiving.csv
    tool: docs/tools/receiving-sheet.md
    check: python docs/tools/checks/csv-has-columns.py work/receiving.csv po sku qty
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [recv-raw]
    produces: recv-pack
    produce_path: out/receiving.md
    tool: docs/tools/receiving-sheet.md
    check: python docs/tools/checks/file-exists.py out/receiving.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects this shop (**remember**).
