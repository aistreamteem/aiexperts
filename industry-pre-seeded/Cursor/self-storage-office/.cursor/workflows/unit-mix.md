# Unit Mix

**When to use:** From the unit-mix CSV, count units by size and climate versus standard as they coded them. Do not merge types if the sheet splits them. Blank size is an ask, not a photo guess. Occupied versus vacant counts, if included, still come from their columns. Python may write a mix bar chart if they named the question; do not claim why a size is slow. They decide what to advertise. You list mix and questions.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put the unit-mix CSV in `in/`. Read this file and `docs/tools/unit-mix-csv.md`. Walk one ready YAML step (or the whole job if requested): produce the file under this Work Item’s `work/` or `out/`, run the check, then journal-keeper. Do not skip a step with a chat summary.

**Initial phase:** `role-job`

## Work map

```yaml
id: unit-mix
steps:
  - id: mix
    needs: []
    produces: mix
    produce_path: work/unit-mix.csv
    tool: docs/tools/unit-mix-csv.md
    check: python docs/tools/checks/csv-has-columns.py work/unit-mix.csv unit size
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [mix]
    produces: mix-pack
    produce_path: out/unit-mix.md
    tool: docs/tools/unit-mix-csv.md
    check: python docs/tools/checks/file-exists.py out/unit-mix.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects this shop via **remember**.
