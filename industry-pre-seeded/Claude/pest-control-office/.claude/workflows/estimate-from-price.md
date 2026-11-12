# Estimate From Price

**When to use:** Draft estimate lines from their price file and the lead or ticket they stored. Quantity they listed times unit price they listed. Blank price or blank qty: ask. Do not invent a mix, an EPA number, or a monthly rate. Do not promise eradication. Label the pack draft until they accept. They send the proposal. You do not treat the draft as sold work on a route day.

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
id: estimate-from-price
steps:
  - id: price
    needs: []
    produces: price
    produce_path: work/price-file.csv
    tool: docs/tools/price-file.md
    check: python docs/tools/checks/csv-has-columns.py work/price-file.csv item price
    on_fail: retry
    next: [tickets]
  - id: tickets
    needs: [price]
    produces: tickets
    produce_path: work/estimate-tickets.csv
    tool: docs/tools/ticket-sheet.md
    check: python docs/tools/checks/file-exists.py work/estimate-tickets.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [price, tickets]
    produces: estimate-pack
    produce_path: out/estimate.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/estimate.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this shop.
