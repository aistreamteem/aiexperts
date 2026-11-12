# Tuition From File

**When to use:** List amounts, due dates, and payment codes from their tuition sheet. Do not invent a rate, late fee, or refund. Do not collect. Aid rows appear only if their sheet already names them. Holds that block transcripts stay visible if the sheet has a hold column. They invoice. You pack the list and exceptions. Sibling discounts and late fees appear only as printed. You do not dunn. NSF as their code stays a code, not a collections opinion. They invoice. You list exceptions.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put source files in `in/`. Walk one ready YAML step (or the whole named job if requested): produce the file, run the check, then **journal-keeper**.

**Initial phase:** `role-job`

## Work map

```yaml
id: tuition-from-file
steps:
  - id: sheet
    needs: []
    produces: tuition
    produce_path: work/tuition.csv
    tool: docs/tools/tuition-sheet.md
    check: python docs/tools/checks/csv-has-columns.py work/tuition.csv student
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [tuition]
    produces: tuition-pack
    produce_path: out/tuition-from-file.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/tuition-from-file.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this office (use **remember**).
