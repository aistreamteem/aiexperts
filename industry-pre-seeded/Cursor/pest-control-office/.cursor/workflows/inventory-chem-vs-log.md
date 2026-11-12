# Inventory Chem Vs Log

**When to use:** Compare their chemical inventory sheet to application-log product names they already wrote. Flag products logged that are not on the inventory key, and inventory rows with no matching log name if they asked. Do not invent on-hand qty. Do not invent an EPA number or a mix. Short counts stay visible. They buy and they count. You write the mismatch list and a pack the check can see.

## How to run

This file is the whole job. **continue** and **workflow-selector** walk it.

1. Confirm or open a Work Item under `work-items/<id>/` (use **workflow-selector** if none is active). Record this job id as the workflow type.
2. Load `facts/MEMORY-INDEX.md`, then `facts/facts-operations.md` and `facts/rules-operations.md`. Load Work Item facts/rules if present.
3. Put operator files in `work-items/<id>/in/`. Working extracts go in `work-items/<id>/work/`. Finished packs go in `work-items/<id>/out/`. Check logs go in `work-items/<id>/evidence/`.
4. Read only the tool docs named on each step.
5. Walk steps in order. Rewrite every `work/` and `out/` path so it sits under the Work Item folder. Do not start a step whose `needs` files are missing — ask.
6. After each step, run the listed check from the expert root with those rewritten paths. The step passes only when the check exits 0. On fail, retry at most 3 times, then ask. If a step has no check, propose a check and get operator approval before marking it passed.
7. Update the Work Item journal with **journal-keeper**. Missing shop knowledge: ask; do not invent. Requests outside `MyRole.txt`: refuse and stop.

**Initial phase:** `role-job`

## Work map

```yaml
id: inventory-chem-vs-log
steps:
  - id: inv
    needs: []
    produces: inv
    produce_path: work/inventory-chem.csv
    tool: docs/tools/inventory-chem.md
    check: python docs/tools/checks/csv-has-columns.py work/inventory-chem.csv product qty
    on_fail: retry
    next: [log]
  - id: log
    needs: [inv]
    produces: log
    produce_path: work/chemical-log.csv
    tool: docs/tools/chemical-log.md
    check: python docs/tools/checks/file-exists.py work/chemical-log.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [inv, log]
    produces: inv-log-pack
    produce_path: out/inventory-vs-log.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/inventory-vs-log.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this shop.
