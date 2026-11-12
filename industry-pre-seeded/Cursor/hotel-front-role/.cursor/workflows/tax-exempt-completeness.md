# Tax Exempt Completeness

**When to use:** Compare folios coded tax-exempt to certificates in the tax-file folder. List present, missing, expired, and name-mismatch. Do not decide exemption as law and do not invent a zero tax. Tax-off without a cert stays an exception. They apply or reverse tax. You deliver the completeness list and write-up. Name-mismatch and expired letters count as missing. You do not accept a verbal exemption. Occupancy tax stays their file, not a legal opinion.

**How to run:** Self-contained for **continue** / **workflow-selector**.

1. Confirm an active Work Item under `work-items/<id>/`. Put source files in `in/`.
2. Load `facts/MEMORY-INDEX.md`, then operations facts/rules, plus Work Item facts/rules if present.
3. Walk the steps below in order. Paths (`work/`, `out/`) are relative to `work-items/<id>/`. For each step: read the named tool doc, write the artifact, run the check. Missing needs → ask. Check fail → retry at most 3, then ask.
4. After the pack step, leave the finished list plus a short pack in `out/` (docs used, artifacts, checks, open asks).
5. **journal-keeper**. One ready step per **continue** unless they asked for the whole named job.

**Initial phase:** `role-job`

## Work map

```yaml
id: tax-exempt-completeness
steps:
  - id: folios
    needs: []
    produces: folios
    produce_path: work/folio-index.csv
    tool: docs/tools/folio-pdf.md
    check: python docs/tools/checks/file-exists.py work/folio-index.csv
    on_fail: retry
    next: [tax]
  - id: tax
    needs: [folios]
    produces: tax
    produce_path: work/tax-file.csv
    tool: docs/tools/tax-file.md
    check: python docs/tools/checks/file-exists.py work/tax-file.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [folios, tax]
    produces: exempt-pack
    produce_path: out/tax-exempt-completeness.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/tax-exempt-completeness.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator confirms how *this* property works.
