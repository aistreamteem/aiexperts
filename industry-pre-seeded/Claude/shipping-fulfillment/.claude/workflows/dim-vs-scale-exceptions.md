# DIM versus Scale Exceptions

**When to use:** Compare carton-size inches to scale-export pounds. List gaps versus billed weight only if a carrier invoice file is already in the folder. Never invent DIM, scale weight, or billed weight. Never apply a divisor they did not write. Ask if dimensions are missing. They measure and they dispute. You do not pay the DIM charge. Catalog inches and scale pounds stay on separate columns. Billed weight appears only from an invoice file they already stored. They measure again if they choose. You do not pay the DIM invoice.

**How to run:** Open or switch to a Work Item under `work-items/<id>/`. Put source files in that item’s `in/`. Follow the YAML steps below — one ready step per **continue**, or the whole named job if requested. Read the named `docs/tools/` doc. Produce files under this Work Item. Run each step’s check. Then **journal-keeper**.

**Initial phase:** `role-job`

## Work map

```yaml
id: dim-vs-scale-exceptions
steps:
  - id: scale
    needs: []
    produces: scale
    produce_path: work/scale.csv
    tool: docs/tools/scale-export.md
    check: python docs/tools/checks/csv-has-columns.py work/scale.csv weight
    on_fail: retry
    next: [sizes]
  - id: sizes
    needs: [scale]
    produces: sizes
    produce_path: work/carton-sizes.csv
    tool: docs/tools/carton-size-sheet.md
    check: python docs/tools/checks/file-exists.py work/carton-sizes.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [scale, sizes]
    produces: dim-pack
    produce_path: out/dim-vs-scale.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/dim-vs-scale.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they **remember** a shop correction.
