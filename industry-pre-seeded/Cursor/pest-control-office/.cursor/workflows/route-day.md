# Route Day

**When to use:** Build a day list from their route CSV and tickets: tech, account, service, window, pet, child, dog, and skip flags. Apply the skip list first. Do not invent a ticket, a target pest, a mix, or a license stamp. Wind stays on the board until they write a hold. One account per row. They dispatch. You write the list and a short pack. Gate codes stay out of the pack.

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
id: route-day
steps:
  - id: route
    needs: []
    produces: route
    produce_path: work/route.csv
    tool: docs/tools/route-csv.md
    check: python docs/tools/checks/csv-has-columns.py work/route.csv route account
    on_fail: retry
    next: [tickets]
  - id: tickets
    needs: [route]
    produces: tickets
    produce_path: work/tickets.csv
    tool: docs/tools/ticket-sheet.md
    check: python docs/tools/checks/csv-has-columns.py work/tickets.csv ticket account
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [route, tickets]
    produces: route-day-pack
    produce_path: out/route-day.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/route-day.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this shop.
