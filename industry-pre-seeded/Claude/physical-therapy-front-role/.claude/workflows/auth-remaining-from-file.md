# Auth Remaining From File

**When to use:** From their auth tracker and visit-count export, list authorized, used, and remaining only as those files already show. No screenshot or tracker remaining column: ask. Do not invent remaining and do not subtract in your head unless you are copying their remaining column. Quote letter dates when they attached a letter. Least PHI on the sheet. A quoted remaining figure is not a promise the plan will pay. Produce the CSV in `out/`.

**How to run:** Open or switch to a Work Item under `work-items/<id>/`. Follow this YAML with **continue** (one ready step, or the whole named job if requested). Read the named `docs/tools/` file. Write artifacts under this Work Item. Run each step’s check. **journal-keeper** after the step.

**Initial phase:** `role-job`

## Work map

```yaml
id: auth-remaining-from-file
steps:
  - id: tracker
    needs: []
    produces: auth
    produce_path: work/auth-tracker.csv
    tool: docs/tools/auth-tracker.md
    check: python docs/tools/checks/csv-has-columns.py work/auth-tracker.csv chart remaining
    on_fail: retry
    next: [counts]
  - id: counts
    needs: [auth]
    produces: counts
    produce_path: work/visit-counts.csv
    tool: docs/tools/visit-count-export.md
    check: python docs/tools/checks/file-exists.py work/visit-counts.csv
    on_fail: retry
    next: [write]
  - id: write
    needs: [auth, counts]
    produces: auth-writeup
    produce_path: out/auth-remaining.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/auth-remaining.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this clinic.
