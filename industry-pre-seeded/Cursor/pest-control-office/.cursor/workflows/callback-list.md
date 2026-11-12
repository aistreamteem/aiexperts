# Callback List

**When to use:** List open callbacks from their callback file and matching tickets. Attach named photos if present. Do not diagnose a structure or a species. Do not promise eradication. Warranty versus courtesy versus billable follows their warranty file. Hours come from their sheet, not invented time. Skip and pet flags still apply. They schedule the return. You write the list and questions.

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
id: callback-list
steps:
  - id: callbacks
    needs: []
    produces: callbacks
    produce_path: work/callbacks.csv
    tool: docs/tools/callback-list.md
    check: python docs/tools/checks/csv-has-columns.py work/callbacks.csv ticket account
    on_fail: retry
    next: [tickets]
  - id: tickets
    needs: [callbacks]
    produces: tickets
    produce_path: work/callback-tickets.csv
    tool: docs/tools/ticket-sheet.md
    check: python docs/tools/checks/file-exists.py work/callback-tickets.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [callbacks, tickets]
    produces: callback-pack
    produce_path: out/callbacks.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/callbacks.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this shop.
