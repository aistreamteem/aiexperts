# Auth remaining from file

**When to use:** From their auth tracker and visit-count export, list authorized, used, and remaining only as those files already show. No screenshot or tracker remaining column: ask. Do not invent remaining and do not subtract in your head unless you are copying their remaining column. Quote letter dates when they attached a letter. Least PHI on the sheet. A quoted remaining figure is not a promise the plan will pay. Produce the CSV plus a write-up.

**How to run:** Open or reuse `work-items/<id>/`. Put source files in `in/`. Follow this map in order: read the named `docs/tools/` file, write `produce_path` inside this Work Item, run the step `check`, retry at most 3 times on fail then ask. Pass produced files to the next step. One ready step per continue unless the operator asked for the whole job. Then journal-keeper.

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

Starter work map. Replace tools and checks when the operator confirms how this clinic works.
