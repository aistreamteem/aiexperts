# Leftover-form completeness

**When to use:** For events whose leftover policy requires a signed release, list form present or missing from the leftover-form folder against the event-order list. Do not invent legal text. Do not stamp leftovers safe. Drop-off jobs follow their policy file, which may not require a form. Write-up is a completeness list, not a donation finding. They collect signatures. You keep missing forms visible.

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
id: leftover-form-completeness
steps:
  - id: orders
    needs: []
    produces: orders
    produce_path: work/leftover-events.csv
    tool: docs/tools/event-order-pdf.md
    check: python docs/tools/checks/csv-has-columns.py work/leftover-events.csv event date
    on_fail: retry
    next: [forms]
  - id: forms
    needs: [orders]
    produces: forms
    produce_path: work/leftover-forms.csv
    tool: docs/tools/leftover-form-folder.md
    check: python docs/tools/checks/file-exists.py work/leftover-forms.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [orders, forms]
    produces: leftover-pack
    produce_path: out/leftover-form-completeness.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/leftover-form-completeness.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct the shop and **remember**.
