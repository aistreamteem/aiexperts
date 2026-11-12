# New-hire completeness

**When to use:** Read their new-hire checklist sheet and the packet folder. Mark each row present, missing, or not-applicable as they allow. Pull I-9 section dates from the index as dates only. Start date, title, and wage come from their offer or hire sheet — do not invent them. No SSN, no account numbers, no ID images in docs/. Write the missing-forms list and a pack summary under `out/`. They collect the missing pages. You do not clear the person to work as counsel.

## How to run

1. Open or switch to one Work Item under `work-items/<id>/` (`workflow-selector` if the job is not selected yet). Put source files in that item's `in/`.
2. Follow this file's YAML: one ready step per **continue**, or the whole named job if the operator requested it. Read the named `docs/tools/` doc. Write `produce_path` under this Work Item. Run the step `check`. Retry at most three times, then ask.
3. Run **journal-keeper** after the step (or job) completes.

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

Starter work map. Replace tools and checks when they correct this shop.
