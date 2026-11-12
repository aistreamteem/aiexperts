# Small multiples from a facet they name

**When to use:** Repeat the same chart for each value of the facet column they named. Write the aggregated work CSV, one faceted PNG, and a write-up that states shared versus free y-scale and n per panel. Do not drop a small panel. Do not invent a facet. A folder of files is the dashboard, not a BI site. If seaborn is missing, matplotlib subplots or an install ask — do not fake panels.

**Initial phase:** `question`

**Method:** `docs/role/work-item-method.md` — faceted comparison.

## How to run

This file is self-contained. Walk it with **continue** / **journal-keeper**.

1. Confirm an active Work Item under `work-items/<id>/`. Paths below are **inside that folder**.
2. **Question gate:** they named the facet column and the inner chart (same measure and form in every panel). Shared vs free y-scale is an ask or a stated default.
3. Put the source file in `in/`. Load `docs/tools/pandas.md` and `docs/tools/seaborn.md`.
4. Do one ready step per continue unless they asked for the whole job.
5. For each step: produce the file, run the check from the Work Item folder, log under `evidence/`. Retry at most three times, then ask.
6. **journal-keeper** after the step.

## Work map

```yaml
id: small-multiples
steps:
  - id: facet
    needs: []
    produces: facet
    produce_path: work/small-multiples.csv
    tool: docs/tools/pandas.md
    check: python docs/tools/checks/csv-has-columns.py work/small-multiples.csv facet date value
    on_fail: retry
    next: [chart]
  - id: chart
    needs: [facet]
    produces: png
    produce_path: out/small-multiples.png
    tool: docs/tools/seaborn.md
    check: python docs/tools/checks/file-exists.py out/small-multiples.png
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [png]
    produces: writeup
    produce_path: out/small-multiples.md
    tool: docs/tools/chart-output-folder.md
    check: python docs/tools/checks/file-exists.py out/small-multiples.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they teach.
