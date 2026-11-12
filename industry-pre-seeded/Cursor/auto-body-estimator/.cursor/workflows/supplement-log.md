# Supplement log

**When to use:** List estimate versions from the supplement log and join to the estimate export so first-write versus later dollars stay visible. Do not invent a supplement. Do not hide an insurer reduction. Aging days come from their dates, not a promised SLA. Write-up is the version list plus asks, not a totaling verdict and not a promise the carrier will pay.

**How to run:** Confirm the Work Item under `work-items/<id>/`. Walk the YAML steps in this file via **continue** (one ready step, or the whole named job if requested). Read the cited `docs/tools/` file, write artifacts under this Work Item's `work/` and `out/`, run the step `check` against those paths, then **journal-keeper**.

**Initial phase:** first YAML step in this file

## Work map

```yaml
id: supplement-log
steps:
  - id: log
    needs: []
    produces: log
    produce_path: work/supplement-log.csv
    tool: docs/tools/supplement-log.md
    check: python docs/tools/checks/csv-has-columns.py work/supplement-log.csv claim date
    on_fail: retry
    next: [est]
  - id: est
    needs: [log]
    produces: est
    produce_path: work/estimate-export.csv
    tool: docs/tools/estimate-export.md
    check: python docs/tools/checks/file-exists.py work/estimate-export.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [log, est]
    produces: supp-pack
    produce_path: out/supplement-log.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/supplement-log.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects this shop's process (**remember**).
