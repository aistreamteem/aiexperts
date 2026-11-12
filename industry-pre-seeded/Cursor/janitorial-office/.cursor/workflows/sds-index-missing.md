# SDS Index Missing

**When to use:** Compare chemical names on the par sheet to the SDS index. List products with no index row or a missing-file flag. Do not invent a mix or download a sheet as their official file unless they named the fetch. Do not stamp Hazard Communication complete. Write-up is the gap list. They file SDS PDFs. You pack present versus missing the check can see.

**How to run:** Use **continue** with this workflow. Work inside `work-items/<id>/`. For each step: read the tool doc, produce the file, run the check (retry at most 3, then ask), then **journal-keeper**. Do not invent a mix or stamp Hazard Communication complete.

**Initial phase:** `index`

## Work map

```yaml
id: sds-index-missing
steps:
  - id: index
    needs: []
    produces: index
    produce_path: work/sds-index.csv
    tool: docs/tools/sds-index.md
    check: python docs/tools/checks/file-exists.py work/sds-index.csv
    on_fail: retry
    next: [pars]
  - id: pars
    needs: [index]
    produces: pars
    produce_path: work/chemical-par.csv
    tool: docs/tools/supply-par-sheet.md
    check: python docs/tools/checks/file-exists.py work/chemical-par.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [index, pars]
    produces: sds-pack
    produce_path: out/sds-missing.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/sds-missing.md
    on_fail: retry
    next: []
```

Starter map. Replace tools and checks when the operator corrects this shop (**remember**).
