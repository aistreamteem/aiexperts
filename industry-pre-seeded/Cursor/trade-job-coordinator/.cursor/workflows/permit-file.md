# Permit File

**When to use:** For jobs they marked as needing a permit: number, AHJ, dates. Do not say passed unless the file says passed and dated. Scheduled is not passed. Copy applied, issued, and result-as-written from the card or screenshot they saved. HOA paper is a second row if they track it. Do not invent a number or a city. You do not inspect. Correction lists stay as written. Missing number on a flagged job is a question. The pack quotes their file only.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put source files in `in/`. Walk one ready YAML step (or the whole named job if requested): produce the file, run the check, then **journal-keeper**.

**Initial phase:** `role-job`

## Work map

```yaml
id: permit-file
steps:
  - id: jobs
    needs: []
    produces: permit-jobs
    produce_path: work/permit-jobs.csv
    tool: docs/tools/permit-log.md
    check: python docs/tools/checks/file-exists.py work/permit-jobs.csv
    on_fail: retry
    next: [numbers]
  - id: numbers
    needs: [permit-jobs]
    produces: permit-numbers
    produce_path: work/permit-numbers.csv
    tool: docs/tools/permit-log.md
    check: python docs/tools/checks/csv-has-columns.py work/permit-numbers.csv job permit_number status
    on_fail: retry
    next: [permit-pack]
  - id: permit-pack
    needs: [permit-numbers]
    produces: permit-writeup
    produce_path: out/permit-file.md
    tool: docs/tools/permit-log.md
    check: python docs/tools/checks/file-exists.py out/permit-file.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this shop (**remember**).
