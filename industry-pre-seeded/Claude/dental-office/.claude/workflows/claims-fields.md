# Claims Fields

**When to use:** List missing claim fields and named attachments from the claim images they provide. Do not adjudicate or choose CDT codes. Do not fill tooth or surface from a film. Do not promise the plan will pay. Copy subscriber versus patient as printed. Date of service and submitted date stay separate if both appear. Name attachment filenames or say missing. Do not copy a full SSN or extra clinical narrative into the tracking sheet. Clearinghouse accepted is not paid.

**How to run:** Open or reuse `work-items/<id>/`. Put the source export in `in/`. Follow this map in order: read the named `docs/tools/` file, write `produce_path` inside this Work Item, run the step `check`, retry at most 3 times on fail then ask. Pass produced files to the next step. One ready step per continue unless the operator asked for the whole job. Then journal-keeper.

**Initial phase:** `role-job`

## Work map

```yaml
id: claims-fields
steps:
  - id: pull
    needs: []
    produces: claims-raw
    produce_path: work/claims.csv
    tool: docs/tools/claim-form-pdf.md
    check: python docs/tools/checks/file-exists.py work/claims.csv
    on_fail: retry
    next: [columns]
  - id: columns
    needs: [claims-raw]
    produces: claims-cols
    produce_path: work/claims.csv
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/csv-has-columns.py work/claims.csv claim_id status
    on_fail: retry
    next: [write]
  - id: write
    needs: [claims-cols]
    produces: claims-writeup
    produce_path: out/claims-check.md
    tool: docs/tools/claim-form-pdf.md
    check: python docs/tools/checks/file-exists.py out/claims-check.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator confirms how this office works.
