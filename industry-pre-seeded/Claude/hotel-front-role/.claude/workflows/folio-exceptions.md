# Folio Exceptions

**When to use:** Read folio PDFs against the tax file and any package or routing notes they stored. List missing posts, duplicates, tax-off without a cert, comps without a code, and POS mismatches. Never invent a correcting amount or a tax. Stop and ask if PAN is visible. They adjust folios. You deliver the exception list and write-up. Package-split misses and city-ledger routing errors belong on the same list when the files show them. Do not hide a miss to tidy night audit. Min-necessary guest labels only.

**How to run:** Self-contained for **continue** / **workflow-selector**.

1. Confirm an active Work Item under `work-items/<id>/`. Put folio PDFs and the tax file in `in/`.
2. Load `facts/MEMORY-INDEX.md`, then operations facts/rules, plus Work Item facts/rules if present.
3. Walk the steps below in order. Paths (`work/`, `out/`) are relative to `work-items/<id>/`. For each step: read the named tool doc, write the artifact, run the check. Missing needs → ask. Check fail → retry at most 3, then ask.
4. After the pack step, leave the finished list plus a short write-up in `out/` (docs used, artifacts, checks, open asks).
5. **journal-keeper**. One ready step per **continue** unless they asked for the whole named job.

**Initial phase:** `role-job`

## Work map

```yaml
id: folio-exceptions
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
    produces: folio-pack
    produce_path: out/folio-exceptions.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/folio-exceptions.md
    on_fail: retry
    next: []
```

Starter step list. Replace tools and checks when they correct this property (**remember**).
