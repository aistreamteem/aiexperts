# Inventory Completeness

**When to use:** Compare the inventory sheet to rooms, PBO versus CP codes, and the high-value list if their rule requires one. Flag missing rooms, blank cube columns, and “see photos” with no photo. Do not invent a piece, a cube, or a pound. Photos they stored get an index; you do not invent a shot. They resurvey. You write the hole list the check can see.

**How to run:** This file is the instruction. After **workflow-selector** records this job:

1. Confirm `work-items/<id>/` exists. Operator inventory and photos go in `in/`.
2. For the next ready step, read the named tool under `docs/tools/`.
3. Write the artifact inside the Work Item folder.
4. Run the check from the Work Item folder. Exit 0 = pass. On fail, retry at most 3 times, then ask.
5. **journal-keeper**. One ready step per **continue** unless they asked for the whole job.

**Human gates:** Operator resurveys missing rooms. Operator supplies photos if the sheet says “see photos.” Blank cube stays blank.

**Initial phase:** `role-job` (method phase: inventory)

## Work map

```yaml
id: inventory-completeness
steps:
  - id: inv
    needs: []
    produces: inv
    produce_path: work/inventory.csv
    tool: docs/tools/inventory-sheet.md
    check: python docs/tools/checks/csv-has-columns.py work/inventory.csv job item qty
    on_fail: retry
    next: [photos]
  - id: photos
    needs: [inv]
    produces: photos
    produce_path: work/photo-index.csv
    tool: docs/tools/photo-folder.md
    check: python docs/tools/checks/file-exists.py work/photo-index.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [inv, photos]
    produces: inv-pack
    produce_path: out/inventory-completeness.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/inventory-completeness.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator confirms how *this* shop files.
