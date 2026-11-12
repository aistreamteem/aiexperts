# BOL Pack

**When to use:** Assemble a bill-of-lading completeness pack from their BOL PDF, scale export, and NMFC file. Copy weight and class only when those files have them. Ask on missing ship-to, piece count, or prepaid/collect/third-party. Never invent NMFC class or weight. Never sign as hazmat certifier. They tender. You do not pay the freight bill. Third-party account blanks stay asks. Hazmat lines need their hazmat file and still get no certifier stamp from you. They tender the freight. You never pay the carrier.

**How to run:** Open or switch to a Work Item under `work-items/<id>/`. Put source files in that item’s `in/`. Follow the YAML steps below — one ready step per **continue**, or the whole named job if requested. Read the named `docs/tools/` doc. Produce files under this Work Item. Run each step’s check. Then **journal-keeper**.

**Initial phase:** `role-job`

## Work map

```yaml
id: bol-pack
steps:
  - id: bol
    needs: []
    produces: bol
    produce_path: work/bol.pdf
    tool: docs/tools/bol-pdf.md
    check: python docs/tools/checks/file-exists.py work/bol.pdf
    on_fail: retry
    next: [scale]
  - id: scale
    needs: [bol]
    produces: scale
    produce_path: work/scale.csv
    tool: docs/tools/scale-export.md
    check: python docs/tools/checks/csv-has-columns.py work/scale.csv weight
    on_fail: retry
    next: [nmfc]
  - id: nmfc
    needs: [scale]
    produces: nmfc
    produce_path: work/nmfc.csv
    tool: docs/tools/nmfc-file.md
    check: python docs/tools/checks/file-exists.py work/nmfc.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [bol, scale, nmfc]
    produces: bol-pack
    produce_path: out/bol-pack.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/bol-pack.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they **remember** a shop correction.
