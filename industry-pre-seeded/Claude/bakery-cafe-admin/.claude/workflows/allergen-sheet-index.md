# Allergen Sheet Index

**When to use:** Index their allergen sheet against formula or bake-list names: missing rows, two-sheet fights, blank sesame or nut cells. Quote contains and may-contain exactly. Do not invent status. Do not write gluten-free as a legal claim. Do not advise a guest. FDA pages stay orientation. The pack is the hole list. Blank cells stay blank. They own the live matrix; you index holes.

**How to run:** Self-contained. Active Work Item under `work-items/<id>/`. For each ready step: read the tool doc → write `produce_path` inside that Work Item → run the check with working directory = the Work Item folder → journal-keeper. Two-sheet fights and blank sesame/nut cells are human gates.

**Initial phase:** `sheet`

## Work map

```yaml
id: allergen-sheet-index
steps:
  - id: sheet
    needs: []
    produces: allergens
    produce_path: work/allergen-sheet.csv
    tool: docs/tools/allergen-sheet.md
    check: python docs/tools/checks/file-exists.py work/allergen-sheet.csv
    on_fail: retry
    next: [formulas]
  - id: formulas
    needs: [allergens]
    produces: formulas
    produce_path: work/formula-index.csv
    tool: docs/tools/formula-file.md
    check: python docs/tools/checks/file-exists.py work/formula-index.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [allergens, formulas]
    produces: allergen-pack
    produce_path: out/allergen-sheet-index.md
    tool: docs/tools/allergen-sheet.md
    check: python docs/tools/checks/file-exists.py out/allergen-sheet-index.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator confirms how this shop files (`remember` / `integrate-docs`).
