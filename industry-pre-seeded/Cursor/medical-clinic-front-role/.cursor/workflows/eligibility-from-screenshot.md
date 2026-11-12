# Eligibility from screenshot

**When to use:** Quote only the dated screenshot or clearinghouse print they saved: plan name, active wording, copay or deductible sentences as printed, image date. No screenshot: ask. Do not invent remaining benefits and do not promise the plan will pay. If the image is cropped, stale, or for the wrong member, ask for a dated full page. Least PHI on the quote sheet. They verify; you do not log into the payer portal. Card images are not eligibility.

**How to run:** Open or reuse `work-items/<id>/`. Follow this file’s YAML one ready step (or the whole named job if requested). Then **journal-keeper**.

**Initial phase:** `role-job`

## Work map

```yaml
id: eligibility-from-screenshot
steps:
  - id: shots
    needs: []
    produces: elig
    produce_path: work/eligibility.csv
    tool: docs/tools/eligibility-screenshot-folder.md
    check: python docs/tools/checks/file-exists.py work/eligibility.csv
    on_fail: retry
    next: [columns]
  - id: columns
    needs: [elig]
    produces: elig-cols
    produce_path: work/eligibility.csv
    tool: docs/tools/eligibility-screenshot-folder.md
    check: python docs/tools/checks/csv-has-columns.py work/eligibility.csv chart date
    on_fail: retry
    next: [write]
  - id: write
    needs: [elig-cols]
    produces: elig-writeup
    produce_path: out/eligibility.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/eligibility.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator confirms how *this* clinic works (**remember**).
