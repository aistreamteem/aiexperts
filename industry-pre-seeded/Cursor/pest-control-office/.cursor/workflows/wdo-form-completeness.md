# WDO Form Completeness

**When to use:** Check their WDO or termite form pack: form fields, graph present, photos named if they require them. Do not stamp the inspection. Do not diagnose the structure. Do not invent findings or a moisture reading. Missing graph or missing signature stays a hole. Real-estate deadlines they wrote stay visible. They inspect and they sign. You write the completeness list and a pack.

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
id: wdo-form-completeness
steps:
  - id: tickets
    needs: []
    produces: tickets
    produce_path: work/wdo-tickets.csv
    tool: docs/tools/ticket-sheet.md
    check: python docs/tools/checks/csv-has-columns.py work/wdo-tickets.csv ticket account
    on_fail: retry
    next: [photos]
  - id: photos
    needs: [tickets]
    produces: photos
    produce_path: work/wdo-photo-index.csv
    tool: docs/tools/photo-folder.md
    check: python docs/tools/checks/file-exists.py work/wdo-photo-index.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [tickets, photos]
    produces: wdo-pack
    produce_path: out/wdo-completeness.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/wdo-completeness.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this shop.
