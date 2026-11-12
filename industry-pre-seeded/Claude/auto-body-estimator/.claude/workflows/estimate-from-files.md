# Estimate pack from their files

**When to use:** Build an estimate pack from their labor matrix, parts file, and estimate export. Hours come only from the matrix or listed operations. Prices come only from the parts file. Do not invent hours or prices. Do not issue a total-loss verdict or a structural stamp. Write-up names which lines are first-write versus supplement and which fields were blank asks. Distinct from a mechanical RO estimate pack.

**How to run:** Confirm the Work Item under `work-items/<id>/`. Walk the YAML steps in this file via **continue** (one ready step, or the whole named job if requested). Read the cited `docs/tools/` file, write artifacts under this Work Item’s `work/` and `out/`, run the step `check` against those paths, then **journal-keeper**.

**Initial phase:** first YAML step in this file

## Work map

```yaml
id: estimate-from-files
steps:
  - id: matrix
    needs: []
    produces: matrix
    produce_path: work/labor-matrix.csv
    tool: docs/tools/labor-matrix.md
    check: python docs/tools/checks/csv-has-columns.py work/labor-matrix.csv op hours
    on_fail: retry
    next: [parts]
  - id: parts
    needs: [matrix]
    produces: parts
    produce_path: work/parts-file.csv
    tool: docs/tools/parts-file.md
    check: python docs/tools/checks/csv-has-columns.py work/parts-file.csv part price
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [matrix, parts]
    produces: estimate-pack
    produce_path: out/estimate-from-files.md
    tool: docs/tools/estimate-export.md
    check: python docs/tools/checks/file-exists.py out/estimate-from-files.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects this shop's process (**remember**).
