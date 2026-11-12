# Daily Board

**When to use:** From their schedule file, list today's jobs, assigned tech, and missing packing lists. Do not invent ETAs. Typical US SMB boards also show job type and city; copy those columns as they named them. Installs without a CSV the check can see stay questions, not ready-to-roll. Service may run on truck stock; ask their rule rather than inventing policy. Windows stay the blocks they sold. Emergency rows keep their priority mark. Write the day's pack so gaps are visible before the truck leaves. No clock time they did not give.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put source files in `in/`. Walk one ready YAML step (or the whole named job if requested): produce the file, run the check, then **journal-keeper**.

**Initial phase:** `role-job`

## Work map

```yaml
id: daily-board
steps:
  - id: pull
    needs: []
    produces: jobs-raw
    produce_path: work/jobs-raw.csv
    tool: docs/tools/schedule-sheet.md
    check: python docs/tools/checks/file-exists.py work/jobs-raw.csv
    on_fail: retry
    next: [gaps]
  - id: gaps
    needs: [jobs-raw]
    produces: jobs-gaps
    produce_path: work/jobs-gaps.csv
    tool: docs/tools/packing-list-sheet.md
    check: python docs/tools/checks/csv-has-columns.py work/jobs-gaps.csv job missing
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [jobs-gaps]
    produces: day-pack
    produce_path: out/days-jobs.md
    tool: docs/tools/schedule-sheet.md
    check: python docs/tools/checks/file-exists.py out/days-jobs.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this shop (**remember**).
