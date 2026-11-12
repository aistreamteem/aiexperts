# Disclosure Completeness

**When to use:** Check the disclosure folder against their checklist: seller statement, lead pamphlet receipt if their year-built file puts the property in scope, and any other named state or local pages. Present, signed, dated, or missing only. Do not fill seller answers. Do not invent a year built. Do not give a condition or fair-housing opinion. Buyer acknowledgments stay separate rows if their form uses them. Their checklist wins over a remembered packet. They complete the forms. You list holes.

**How to run:** open or select a Work Item under `work-items/<id>/` → follow this file one ready step (or the whole named job if requested) → journal-keeper

**Initial phase:** `role-job`

## Work map

```yaml
id: disclosure-completeness
steps:
  - id: folder
    needs: []
    produces: disclosures
    produce_path: work/disclosures.csv
    tool: docs/tools/disclosure-folder.md
    check: python docs/tools/checks/csv-has-columns.py work/disclosures.csv document status
    on_fail: retry
    next: [checklist]
  - id: checklist
    needs: [disclosures]
    produces: disclosure-checklist
    produce_path: work/disclosure-checklist.csv
    tool: docs/tools/checklist-sheet.md
    check: python docs/tools/checks/file-exists.py work/disclosure-checklist.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [disclosures, disclosure-checklist]
    produces: disclosure-pack
    produce_path: out/disclosure-completeness.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/disclosure-completeness.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this shop.
