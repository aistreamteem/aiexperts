# Estimate Pack

**When to use:** Build estimate lines from their labor guide or menu plus the parts file they confirmed. Label any missing hour or price as a question. Do not invent book time or mix two guides. Diagnostic fees stay if they sell them. Shop fees copy from their RO settings, not from another store. Quality labels stay as quoted; do not rule OEM safer than aftermarket. Independent menus and dealer factory operations both apply. The pack is not sold work. Auth still required. Ask which matrix is source of truth.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Follow the YAML steps in order: read the named tool doc under `docs/tools/`, write `produce_path` inside this Work Item (`work/` and `out/` mean `work-items/<id>/work/` and `work-items/<id>/out/`), run the listed check against those same paths, then **journal-keeper**. Do not start a step whose `needs` files are missing. On check fail, retry at most three times, then ask. `continue` walks one ready step unless the operator asked for the whole job.

**Initial phase:** `role-job`

## Work map

```yaml
id: estimate-pack
steps:
  - id: guide
    needs: []
    produces: guide-raw
    produce_path: work/labor-lines.csv
    tool: docs/tools/labor-guide.md
    check: python docs/tools/checks/csv-has-columns.py work/labor-lines.csv op hours
    on_fail: retry
    next: [parts]
  - id: parts
    needs: [guide-raw]
    produces: est-parts
    produce_path: work/est-parts.csv
    tool: docs/tools/parts-counter.md
    check: python docs/tools/checks/csv-has-columns.py work/est-parts.csv part price
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [est-parts]
    produces: estimate-pack
    produce_path: out/estimate.md
    tool: docs/tools/labor-guide.md
    check: python docs/tools/checks/file-exists.py out/estimate.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects this shop's process (**remember**).
