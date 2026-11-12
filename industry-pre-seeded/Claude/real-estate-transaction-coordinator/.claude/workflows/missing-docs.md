# Missing Docs

**When to use:** Compare their TC checklist to the files actually in the folder. Mark present, signed, dated, or missing. Do not mark complete on a blank template. Exhibits the contract names but the packet lacks become asks. Lead, title, HOA, lender, and earnest-receipt rows stay separate. Do not invent extra legal documents from another state. Do not add wire instructions to look thorough. The pack names holes. They chase the pages. You do not change the contract to hide a miss.

**How to run:** open or select a Work Item under `work-items/<id>/` → follow this file one ready step (or the whole named job if requested) → journal-keeper

**Initial phase:** `role-job`

## Work map

```yaml
id: missing-docs
steps:
  - id: checklist
    needs: []
    produces: checklist
    produce_path: work/tc-checklist.csv
    tool: docs/tools/checklist-sheet.md
    check: python docs/tools/checks/csv-has-columns.py work/tc-checklist.csv document status
    on_fail: retry
    next: [index]
  - id: index
    needs: [checklist]
    produces: index
    produce_path: work/file-index.csv
    tool: docs/tools/closing-file-index.md
    check: python docs/tools/checks/file-exists.py work/file-index.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [checklist, index]
    produces: missing-pack
    produce_path: out/missing-docs.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/missing-docs.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this shop.
