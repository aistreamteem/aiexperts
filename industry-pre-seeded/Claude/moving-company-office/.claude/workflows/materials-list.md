# Materials List

**When to use:** Pull carton and crate quantities from their materials sheet and the inventory tally they named as live. Do not invent a box count or a materials dollar. PBO cartons they will not supply stay off the pull list if they coded PBO. Charges come from the rate file or materials sheet only. They pull stock. You write the list and questions. Credits follow their written rule, not a guess.

**How to run:** This file is the instruction. After **workflow-selector** records this job:

1. Confirm `work-items/<id>/` exists. Operator materials sheet and inventory go in `in/`.
2. For the next ready step, read the named tool under `docs/tools/`.
3. Write the artifact inside the Work Item folder.
4. Run the check from the Work Item folder. Exit 0 = pass. On fail, retry at most 3 times, then ask.
5. **journal-keeper**. One ready step per **continue** unless they asked for the whole job.

**Human gates:** Operator pulls stock. Missing sheet → ask. Do not reuse last job’s counts.

**Initial phase:** `role-job` (method phase: dispatch)

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

Starter work map. Replace tools and checks when the operator confirms how *this* shop files.
