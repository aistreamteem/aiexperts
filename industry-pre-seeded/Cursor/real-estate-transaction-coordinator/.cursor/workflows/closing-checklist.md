# Closing Checklist

**When to use:** Build a closing completeness pack from the closing index, title folder, lender status, and the printed closing and possession dates. Mark CD or settlement versions by date. Do not mark funded or recorded without their confirmation. Do not attach wire instructions. Do not promise they will close. Cash versus financed labels follow the PDFs. Walkthrough and key notes stay as files, not a condition opinion. They and the closer run the table. You name what is still missing.

**How to run:** open or select a Work Item under `work-items/<id>/` → follow this file one ready step (or the whole named job if requested) → journal-keeper

**Initial phase:** `role-job`

## Work map

```yaml
id: closing-checklist
steps:
  - id: index
    needs: []
    produces: closing-index
    produce_path: work/closing-index.csv
    tool: docs/tools/closing-file-index.md
    check: python docs/tools/checks/csv-has-columns.py work/closing-index.csv document status
    on_fail: retry
    next: [dates]
  - id: dates
    needs: [closing-index]
    produces: closing-dates
    produce_path: work/closing-dates.csv
    tool: docs/tools/dates-calendar.md
    check: python docs/tools/checks/file-exists.py work/closing-dates.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [closing-index, closing-dates]
    produces: closing-pack
    produce_path: out/closing-checklist.md
    tool: docs/tools/title-pdf-folder.md
    check: python docs/tools/checks/file-exists.py out/closing-checklist.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this shop.
