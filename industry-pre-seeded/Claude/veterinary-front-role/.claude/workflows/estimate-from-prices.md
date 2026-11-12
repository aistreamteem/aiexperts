# Estimate From Prices

**When to use:** Fill their estimate template using only items and amounts on their price file. No added clinical lines. Quantity and which lines belong come from the veterinarian or a saved template they named. High-low ranges only if the template has those columns. Label the draft as a draft until their authorization process is done. Confirm the fee-file date. Starter / guess until they teach tabs and named bundles.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put their price file and estimate template in `in/`. Read this file and the named `docs/tools/` doc. Walk one ready YAML step (or the whole job if requested): produce the file under this Work Item’s `work/` or `out/`, run the check, then journal-keeper. Do not skip a step with a chat summary.

**Initial phase:** `role-job`

## Work map

```yaml
id: estimate-from-prices
steps:
  - id: prices
    needs: []
    produces: prices
    produce_path: work/prices.csv
    tool: docs/tools/price-file.md
    check: python docs/tools/checks/file-exists.py work/prices.csv
    on_fail: retry
    next: [draft]
  - id: draft
    needs: [prices]
    produces: est-draft
    produce_path: work/estimate-draft.csv
    tool: docs/tools/estimate-template.md
    check: python docs/tools/checks/csv-has-columns.py work/estimate-draft.csv item amount
    on_fail: retry
    next: [write]
  - id: write
    needs: [est-draft]
    produces: est-writeup
    produce_path: out/estimate.md
    tool: docs/tools/estimate-template.md
    check: python docs/tools/checks/file-exists.py out/estimate.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this clinic.
