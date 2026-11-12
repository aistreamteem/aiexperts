# Applicant file completeness

**When to use:** From their applicant folder index, list each applicant for the opening they named and which required forms are present or missing. Do not rank candidates. Do not decide qualified. Do not use a voluntary EEO form for selection. Do not copy SSN. Referral source stays as they wrote it. Status stays their code. Write the missing-forms list and a pack summary under `out/`. They choose whom to interview. A hired or rejected code is theirs, not a reason you invent.

## How to run

1. Open or switch to one Work Item under `work-items/<id>/` (`workflow-selector` if the job is not selected yet). Put source files in that item's `in/`.
2. Follow this file's YAML: one ready step per **continue**, or the whole named job if the operator requested it. Read the named `docs/tools/` doc. Write `produce_path` under this Work Item. Run the step `check`. Retry at most three times, then ask.
3. Run **journal-keeper** after the step (or job) completes.

**Initial phase:** `role-job`

## Work map

```yaml
id: applicant-file-completeness
steps:
  - id: index
    needs: []
    produces: apps
    produce_path: work/applicant-index.csv
    tool: docs/tools/applicant-folder-index.md
    check: python docs/tools/checks/csv-has-columns.py work/applicant-index.csv name opening
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [apps]
    produces: app-pack
    produce_path: out/applicant-missing.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/applicant-missing.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this shop.
