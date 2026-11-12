# Contractor 1099 Year

**When to use:** Build or refresh a contractor payment list for a year they name (ask fiscal versus calendar). Sum vendor payments from their files, mark W-9 present or missing by path only, and write a tracker pack. No TINs in the sheet. They or their CPA file. No worker-classification opinion and no move from payroll to 1099 to save tax. Do not e-file or upload to IRS FIRE. Do not quote a threshold as this shop's rule unless they taught it. Produce vendor YTD, W-9 status, and the tracker write-up. Starter "service vendor" flags are questions until they teach who is product-only or exempt.

**How to run:** Select this job with workflow-selector (or continue). Use `work-items/<id>/`. Put source files in `in/`. Walk one ready step: read the named tool doc, write the produced file under this Work Item, run the check, then journal-keeper. Do not skip a step with a chat summary. Whole named job only if they asked.

**Initial phase:** `role-job`

## Work map

```yaml
id: contractor-1099-year
steps:
  - id: vendors
    needs: []
    produces: vendor-ytd
    produce_path: work/vendor-ytd.csv
    tool: docs/tools/contractor-1099-sheet.md
    check: python docs/tools/checks/csv-has-columns.py work/vendor-ytd.csv payee amount
    on_fail: retry
    next: [w9-gaps]
  - id: w9-gaps
    needs: [vendor-ytd]
    produces: w9-status
    produce_path: work/w9-status.csv
    tool: docs/tools/contractor-1099-sheet.md
    check: python docs/tools/checks/csv-has-columns.py work/w9-status.csv payee w9_on_file
    on_fail: retry
    next: [tracker-pack]
  - id: tracker-pack
    needs: [w9-status]
    produces: 1099-pack
    produce_path: out/1099-tracker.md
    tool: docs/tools/contractor-1099-sheet.md
    check: python docs/tools/checks/file-exists.py out/1099-tracker.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator confirms how this shop works.
