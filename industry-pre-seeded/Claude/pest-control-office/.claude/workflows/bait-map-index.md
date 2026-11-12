# Bait Map Index

**When to use:** Index bait-station maps they stored to account and ticket. List station ids as written. Do not invent a device or redraw the building as a structural diagnosis. Device-scan exports, if present, stay a later reconcile. Photos named to the map help; they are not a diagnosis. Gate codes stay out of the index. They place stations. You write the index and write-up the check can see.

## How to run

This file is the whole job. **continue** and **workflow-selector** walk it. Do not look for deleted process skills.

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
id: bait-map-index
steps:
  - id: maps
    needs: []
    produces: maps
    produce_path: work/bait-map-index.csv
    tool: docs/tools/bait-map-pdf.md
    check: python docs/tools/checks/file-exists.py work/bait-map-index.csv
    on_fail: retry
    next: [tickets]
  - id: tickets
    needs: [maps]
    produces: tickets
    produce_path: work/bait-tickets.csv
    tool: docs/tools/ticket-sheet.md
    check: python docs/tools/checks/file-exists.py work/bait-tickets.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [maps, tickets]
    produces: map-pack
    produce_path: out/bait-map-index.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/bait-map-index.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this shop.
