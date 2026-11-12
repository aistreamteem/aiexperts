# Retention Boxes

**When to use:** Label and hold flag from their sheet. Do not shred, haul, or invent retention years. Use their schedule if they have one; missing schedule is a question, not a seven-year guess. Litigation hold they named stays held. No SSN pages in work/. Contents stay in their words. IRS recordkeeping pages are orientation, not this shop's law. Ask before any destroy conversation; you still do not destroy.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put source files in `in/`. Walk one ready YAML step (or the whole named job if requested): read the named tool doc, produce the file, run the check, then **journal-keeper**.

**Initial phase:** `role-job`

## Work map

```yaml
id: retention-boxes
steps:
  - id: list
    needs: []
    produces: boxes
    produce_path: work/retention-boxes.csv
    tool: docs/tools/retention-sheet.md
    check: python docs/tools/checks/csv-has-columns.py work/retention-boxes.csv box hold
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [boxes]
    produces: ret-pack
    produce_path: out/retention.md
    tool: docs/tools/retention-sheet.md
    check: python docs/tools/checks/file-exists.py out/retention.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this shop.
