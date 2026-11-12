# Dietary list

**When to use:** Build a per-event dietary list from their dietary sheet, the event order, and the allergen file: counts as they labeled them and flags routed to sheet rows. Do not invent a substitute dish. Do not treat a guest. Do not stamp a plate safe. Math that exceeds the guarantee stays flagged. Missing allergen-sheet rows for a flagged dish are asks. Write-up uses their words. They decide the plate. You route.

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
id: dietary-list
steps:
  - id: diet
    needs: []
    produces: dietary
    produce_path: work/dietary.csv
    tool: docs/tools/dietary-sheet.md
    check: python docs/tools/checks/csv-has-columns.py work/dietary.csv event note
    on_fail: retry
    next: [allergen]
  - id: allergen
    needs: [dietary]
    produces: allergens
    produce_path: work/allergen-rows.csv
    tool: docs/tools/allergen-file.md
    check: python docs/tools/checks/file-exists.py work/allergen-rows.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [dietary, allergens]
    produces: dietary-pack
    produce_path: out/dietary-list.md
    tool: docs/tools/event-order-pdf.md
    check: python docs/tools/checks/file-exists.py out/dietary-list.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct the shop and **remember**.
