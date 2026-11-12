# Parts Ready

**When to use:** Build or check a packing list for one job id they name. SKUs from sold PDF or them, not invented. Compare each line to truck-stock or warehouse source they already track. Special orders need a PO and a promised date tied to that job id. Do not mark on-truck unless the count file says so. Finish and fuel stay as sold. Serials belong on warrantied assemblies if the plate or PDF has them. The write-up lists gaps as questions. A chat kit is not the CSV. They load the truck; you do not.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Walk one ready YAML step (or the whole named job if requested). Produce the file, run the check, then **journal-keeper**.

**Initial phase:** `role-job`

## Work map

```yaml
id: parts-ready
steps:
  - id: list
    needs: []
    produces: packing-list
    produce_path: work/packing-list.csv
    tool: docs/tools/packing-list-sheet.md
    check: python docs/tools/checks/csv-has-columns.py work/packing-list.csv sku qty
    on_fail: retry
    next: [stock]
  - id: stock
    needs: [packing-list]
    produces: packing-status
    produce_path: work/packing-status.csv
    tool: docs/tools/truck-stock.md
    check: python docs/tools/checks/csv-has-columns.py work/packing-status.csv sku qty source
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [packing-status]
    produces: packing-writeup
    produce_path: out/packing-list.md
    tool: docs/tools/parts-vendor.md
    check: python docs/tools/checks/file-exists.py out/packing-list.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this shop (**remember**).
