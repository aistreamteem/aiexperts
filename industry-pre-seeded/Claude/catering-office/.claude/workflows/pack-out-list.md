# Pack-out list

**When to use:** Build a pack-out from the event order, house equipment list, and their pack-out sheet: food lines from the menu file and guarantee, chafers, linens, china, coolers, ice, and labels. Drop-off versus full-service must match the order. Shortages versus house on-hand stay visible. Do not invent a piece or a yield. Do not borrow venue kit unless a saved BEO they filed says the hall provides it. Write-up lists holes and asks. They load the van.

## How to run

This file is the whole job. **continue** and **workflow-selector** walk it. Do not look for deleted process skills.

1. Confirm or open a Work Item under `work-items/<id>/` (use **workflow-selector** if none is active). Record this job id as the workflow type.
2. Load `facts/MEMORY-INDEX.md`, then `facts/facts-operations.md` and `facts/rules-operations.md`. Load Work Item facts/rules if present.
3. Put operator files in `work-items/<id>/in/`. Working extracts go in `work-items/<id>/work/`. Finished packs go in `work-items/<id>/out/`. Check logs go in `work-items/<id>/evidence/`.
4. Read only the tool docs named on each step.
5. Walk steps in order. Rewrite every `work/` and `out/` path so it sits under the Work Item folder. Do not start a step whose `needs` files are missing — ask.
6. After each step, run the listed check from the expert root with those rewritten paths. The step passes only when the check exits 0. On fail, retry at most 3 times, then ask. If a step has no check, propose a check and get operator approval before marking it passed.
7. Update the Work Item journal with **journal-keeper**. Missing shop knowledge: ask; do not invent. Requests outside `MyRole.txt`: refuse and stop.
8. Job is done when every step has a passing check (or a documented exception), the pack exists under `out/`, and holes stay visible.

**Initial phase:** `role-job`


## Work map

```yaml
id: pack-out-list
steps:
  - id: order
    needs: []
    produces: order
    produce_path: work/pack-event.csv
    tool: docs/tools/event-order-pdf.md
    check: python docs/tools/checks/csv-has-columns.py work/pack-event.csv event date
    on_fail: retry
    next: [equip]
  - id: equip
    needs: [order]
    produces: equipment
    produce_path: work/pack-equipment.csv
    tool: docs/tools/equipment-list.md
    check: python docs/tools/checks/csv-has-columns.py work/pack-equipment.csv item qty
    on_fail: retry
    next: [sheet]
  - id: sheet
    needs: [order, equipment]
    produces: packout
    produce_path: work/pack-out.csv
    tool: docs/tools/pack-out-sheet.md
    check: python docs/tools/checks/csv-has-columns.py work/pack-out.csv event item
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [order, equipment, packout]
    produces: pack-out-pack
    produce_path: out/pack-out-list.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/pack-out-list.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct the shop and **remember**.
