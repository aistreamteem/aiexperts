# I-9 reverify dates

**When to use:** From their I-9 index, list people with a reverify-by date and whether that date is past on the calendar they use. Blank reverify cells stay blank; if they marked the person as needing reverification, ask. Do not invent a date from a document type. Do not decide status. Do not recommend firing. No document numbers or SSNs in docs/. The pack is a due list for their process, not an immigration opinion.

## How to run

1. Open or switch to one Work Item under `work-items/<id>/` (`workflow-selector` if the job is not selected yet). Put source files in that item's `in/`.
2. Follow this file's YAML: one ready step per **continue**, or the whole named job if the operator requested it. Read the named `docs/tools/` doc. Write `produce_path` under this Work Item. Run the step `check`. Retry at most three times, then ask.
3. Run **journal-keeper** after the step (or job) completes.

**Initial phase:** `role-job`

## Work map

```yaml
id: reverify-dates
steps:
  - id: index
    needs: []
    produces: i9idx
    produce_path: work/i9-index.csv
    tool: docs/tools/i9-folder-index.md
    check: python docs/tools/checks/csv-has-columns.py work/i9-index.csv name
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [i9idx]
    produces: rev-pack
    produce_path: out/i9-reverify-due.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/i9-reverify-due.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this shop.
