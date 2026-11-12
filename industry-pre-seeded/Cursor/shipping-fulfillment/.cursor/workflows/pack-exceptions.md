# Pack Exceptions

**When to use:** Compare the pack export to the pick file. List short packs, extra packs, unknown carton codes versus the carton-size sheet, and missing scale weights. Do not invent packed qty. Do not write shipped-complete on a short. Kit components that do not match their kit notes stay listed. They decide reship or backorder. You prepare the exception write-up. Carton codes that are not on the size sheet stay listed. Missing scale weight is an ask, not a guessed pound. They decide reship or backorder. You do not hide a short inside packed-complete.

**How to run:** Open or switch to a Work Item under `work-items/<id>/`. Put source files in that item's `in/`. Follow the YAML steps below — one ready step per **continue**, or the whole named job if requested. Read the named `docs/tools/` doc. Produce files under this Work Item. Run each step's check. Then **journal-keeper**.

**Initial phase:** `role-job`

## Work map

```yaml
id: pack-exceptions
steps:
  - id: picks
    needs: []
    produces: picks
    produce_path: work/picks.csv
    tool: docs/tools/pick-csv.md
    check: python docs/tools/checks/csv-has-columns.py work/picks.csv order sku qty
    on_fail: retry
    next: [packs]
  - id: packs
    needs: [picks]
    produces: packs
    produce_path: work/packs.csv
    tool: docs/tools/pack-csv.md
    check: python docs/tools/checks/csv-has-columns.py work/packs.csv order sku qty
    on_fail: retry
    next: [sizes]
  - id: sizes
    needs: [packs]
    produces: sizes
    produce_path: work/carton-sizes.csv
    tool: docs/tools/carton-size-sheet.md
    check: python docs/tools/checks/file-exists.py work/carton-sizes.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [picks, packs, sizes]
    produces: pack-ex-pack
    produce_path: out/pack-exceptions.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/pack-exceptions.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this shop.
