# Submittal Aging

**When to use:** Status and aging from their submittal export. You do not approve, reject, or change for review to approved. Keep specification sections and resubmittal suffixes they used. Missing sections are asks, not guessed numbers. Shop-drawing stamps stay on the files they stored; this pack is the register, not a review. Aging uses their sent and returned dates. The pack names the export and lists open versus returned in their words so the field and office share one list.

**How to run:** Follow `docs/role/work-item-method.md`. Use or create `work-items/<id>/`. Put source files in `in/`. For each YAML step below, in order: (1) do not start if `needs` files are missing — ask the operator; (2) read the `tool` file under `docs/tools/`; (3) write `produce_path` inside this Work Item folder (`work/` and `out/` are relative to the Work Item, not the expert root); (4) run `check` with those same relative paths; (5) on fail, retry at most 3 times then ask via **operator-qa**; (6) update the Work Item journal with **journal-keeper**. After the last step, the pack in `out/` must quote their source files. Do not invent counts, dates, approvals, or answers.

**Initial phase:** `intake`

## Work map

```yaml
id: submittal-aging
steps:
  - id: list
    needs: []
    produces: sub-raw
    produce_path: work/submittals.csv
    tool: docs/tools/submittal-log.md
    check: python docs/tools/checks/csv-has-columns.py work/submittals.csv number status
    on_fail: retry
    next: [age]
  - id: age
    needs: [sub-raw]
    produces: sub-aged
    produce_path: work/submittals-aged.csv
    tool: docs/tools/submittal-log.md
    check: python docs/tools/checks/csv-has-columns.py work/submittals-aged.csv number status
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [sub-aged]
    produces: sub-pack
    produce_path: out/submittals.md
    tool: docs/tools/submittal-log.md
    check: python docs/tools/checks/file-exists.py out/submittals.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they confirm how this shop files.
