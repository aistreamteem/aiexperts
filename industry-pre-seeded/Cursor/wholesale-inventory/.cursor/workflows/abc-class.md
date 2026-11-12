# ABC class worksheet

**When to use:** Class from their stored rules or from a value or movement column they provided. Do not invent annual demand or textbook cut points. Do not relabel a class because a SKU feels important. Class is not quality. If they asked for a worksheet, show the field you used and the thresholds they named. Missing value: ask. Count-frequency talk quotes their rule only. Their master class wins if they did not ask to recompute.

**How to run:** Open or switch to a Work Item under `work-items/<id>/`. Follow this YAML one ready step (or the whole named job if requested). Then **journal-keeper**.

**Initial phase:** `role-job`

## Work map

```yaml
id: abc-class
steps:
  - id: pull
    needs: []
    produces: abc-raw
    produce_path: work/abc-input.csv
    tool: docs/tools/abc-sheet.md
    check: python docs/tools/checks/csv-has-columns.py work/abc-input.csv sku value
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [abc-raw]
    produces: abc-pack
    produce_path: out/abc.md
    tool: docs/tools/abc-sheet.md
    check: python docs/tools/checks/file-exists.py out/abc.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects this shop (**remember**).
