# Supplies

**When to use:** Build or update a supply CSV for them to order. Flag at or below their min. Do not buy, open a cart, or invent a min or SKU. Brand lines come from their last invoice. Kitchen and postage follow the same no-order rule if those rows are on the sheet. Office stock stays off the warehouse count unless they taught one list. Missing on-hand: ask whether they count that item. The write-up is a flag list they can act on; you do not place the vendor order.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put source files in `in/`. Walk one ready YAML step (or the whole named job if requested): read the named tool doc, produce the file, run the check, then **journal-keeper**.

**Initial phase:** `role-job`

## Work map

```yaml
id: supplies
steps:
  - id: list
    needs: []
    produces: supplies
    produce_path: work/supplies.csv
    tool: docs/tools/supply-list.md
    check: python docs/tools/checks/csv-has-columns.py work/supplies.csv item qty
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [supplies]
    produces: sup-pack
    produce_path: out/supplies.md
    tool: docs/tools/supply-list.md
    check: python docs/tools/checks/file-exists.py out/supplies.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this shop.
