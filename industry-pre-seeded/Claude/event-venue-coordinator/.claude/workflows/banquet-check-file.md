# Banquet Check File

**When to use:** Compare each banquet-check PDF to the matching BEO for menu, counts, extras, service charge, and tax as their tax file. List mismatches and unsigned checks. Do not invent a tax rate. Do not mark paid. Do not store PAN. Guarantee versus actual follows their contract file only. They present the check. You deliver the exception pack plus write-up. Unsigned checks and tax lines that disagree with their tax file stay on the exception list. Incidentals need a captain slip when their process requires one. They present the check; you do not store PAN or mark paid.

**How to run:** workflow-selector if no Work Item is active → follow this file one ready step (or whole named job if requested) → write artifacts under `work-items/<id>/` → journal-keeper

**Initial phase:** `role-job`

## Work map

```yaml
id: banquet-check-file
steps:
  - id: checks
    needs: []
    produces: checks
    produce_path: work/banquet-checks.csv
    tool: docs/tools/banquet-check-pdf.md
    check: python docs/tools/checks/file-exists.py work/banquet-checks.csv
    on_fail: retry
    next: [beos]
  - id: beos
    needs: [checks]
    produces: beos
    produce_path: work/beos.csv
    tool: docs/tools/beo-pdf.md
    check: python docs/tools/checks/file-exists.py work/beos.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [checks, beos]
    produces: check-pack
    produce_path: out/banquet-check-file.md
    tool: docs/tools/banquet-check-pdf.md
    check: python docs/tools/checks/file-exists.py out/banquet-check-file.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator teaches this shop (use remember).
