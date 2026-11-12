# Equipment versus events

**When to use:** Compare house equipment on-hand to the same-day event pack-outs: chafers, cambros, urns, china. Flag double-books and shortages. Rentals on a PO are not house on-hand until the PO says they land. Do not invent a piece count. Do not silently assign venue kit. Write-up names the Saturday (or day) and which events collide. They rent or they move a job. You keep the shortage visible.

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
id: equipment-vs-events
steps:
  - id: equip
    needs: []
    produces: equipment
    produce_path: work/house-equipment.csv
    tool: docs/tools/equipment-list.md
    check: python docs/tools/checks/csv-has-columns.py work/house-equipment.csv item qty
    on_fail: retry
    next: [events]
  - id: events
    needs: [equipment]
    produces: events
    produce_path: work/equipment-events.csv
    tool: docs/tools/event-order-pdf.md
    check: python docs/tools/checks/csv-has-columns.py work/equipment-events.csv event date
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [equipment, events]
    produces: equip-pack
    produce_path: out/equipment-vs-events.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/equipment-vs-events.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct the shop and **remember**.
