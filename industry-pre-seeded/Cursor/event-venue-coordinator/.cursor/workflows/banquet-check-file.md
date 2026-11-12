# Banquet check versus BEO

**When to use:** Compare each banquet-check PDF to the matching BEO for menu, counts, extras, service charge, and tax as their tax file. List mismatches and unsigned checks. Do not invent a tax rate. Do not mark paid. Do not store PAN. Guarantee versus actual follows their contract file only. They present the check. You deliver the exception pack. Unsigned checks and tax lines that disagree with their tax file stay on the exception list. Incidentals need a captain slip when their process requires one. They present the check; you do not store PAN or mark paid.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put banquet-check PDFs and matching BEOs in `in/`. Read this file and `docs/tools/banquet-check-pdf.md` / `docs/tools/beo-pdf.md`. Walk one ready YAML step (or the whole job if requested): produce the file under this Work Item’s `work/` or `out/`, run the check, then journal-keeper. Do not skip a step with a chat summary.

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

Starter work map. Replace tools and checks when the operator corrects this shop (remember / integrate-docs).
