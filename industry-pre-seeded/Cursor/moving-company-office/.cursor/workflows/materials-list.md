# Materials list

**When to use:** Pull carton and crate quantities from their materials sheet and the inventory tally they named as live. Do not invent a box count or a materials dollar. PBO cartons they will not supply stay off the pull list if they coded PBO. Charges come from the rate file or materials sheet only. They pull stock. You write the list and questions. Credits follow their written rule, not a guess.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put source files in `in/`. Walk one ready YAML step (or the whole named job if requested): read the named tool, produce the file, run the check, then **journal-keeper**. Do not invent weight, cube, rates, crew names, or delivery hours.

**Initial phase:** `role-job`

## Work map

```yaml
id: materials-list
steps:
  - id: mats
    needs: []
    produces: mats
    produce_path: work/materials.csv
    tool: docs/tools/materials-sheet.md
    check: python docs/tools/checks/csv-has-columns.py work/materials.csv item qty
    on_fail: retry
    next: [inv]
  - id: inv
    needs: [mats]
    produces: inv
    produce_path: work/inventory.csv
    tool: docs/tools/inventory-sheet.md
    check: python docs/tools/checks/file-exists.py work/inventory.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [mats, inv]
    produces: mats-pack
    produce_path: out/materials-list.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/materials-list.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects this shop.
