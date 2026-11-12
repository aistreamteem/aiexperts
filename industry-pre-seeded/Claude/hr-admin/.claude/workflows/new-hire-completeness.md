# New Hire Completeness

**When to use:** Read their new-hire checklist sheet and the packet folder. Mark each row present, missing, or not-applicable as they allow. Pull I-9 section dates from the index as dates only. Start date, title, and wage come from their offer or hire sheet — do not invent them. No SSN, no account numbers, no ID images in docs/. Write the missing-forms list and a short write-up. They collect the missing pages. You do not clear the person to work as counsel.

**How to run:** Select this workflow on a Work Item under `work-items/<id>/`. Follow each YAML step: read the `tool` doc, write `produce_path` in this Work Item, run `check`, retry at most 3 then ask. Update the Work Item journal after each step. One ready step per continue unless they asked for the whole pack.

**Initial phase:** `role-job`

## Work map

```yaml
id: new-hire-completeness
steps:
  - id: sheet
    needs: []
    produces: checklist
    produce_path: work/new-hire-checklist.csv
    tool: docs/tools/new-hire-checklist-sheet.md
    check: python docs/tools/checks/csv-has-columns.py work/new-hire-checklist.csv name start_date
    on_fail: retry
    next: [i9]
  - id: i9
    needs: [checklist]
    produces: i9idx
    produce_path: work/i9-index.csv
    tool: docs/tools/i9-folder-index.md
    check: python docs/tools/checks/file-exists.py work/i9-index.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [checklist, i9idx]
    produces: nh-pack
    produce_path: out/new-hire-missing.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/new-hire-missing.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct how *this* shop files.
