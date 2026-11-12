# Rental PO pack

**When to use:** List open rental POs against events: item, qty, deliver window, return window. Flag missing return times, address holes, and POs that fight house equipment already covering the same count. Do not invent a SKU or a price. Do not pay the vendor. Venue vendors on a saved BEO stay labeled venue. Write-up is a completeness pack, not a catalog. They order. You list fights.

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
id: rental-pos
steps:
  - id: pos
    needs: []
    produces: pos
    produce_path: work/rental-pos.csv
    tool: docs/tools/rental-po.md
    check: python docs/tools/checks/csv-has-columns.py work/rental-pos.csv event item
    on_fail: retry
    next: [events]
  - id: events
    needs: [pos]
    produces: events
    produce_path: work/rental-events.csv
    tool: docs/tools/event-order-pdf.md
    check: python docs/tools/checks/csv-has-columns.py work/rental-events.csv event date
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [pos, events]
    produces: rental-pack
    produce_path: out/rental-pos.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/rental-pos.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct the shop and **remember**.
