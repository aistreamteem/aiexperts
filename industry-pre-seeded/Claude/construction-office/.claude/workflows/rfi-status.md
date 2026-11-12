# RFI Status

**When to use:** From their RFI export, list open, overdue versus their due column, and returned. Do not answer design questions or pick a detail. Keep their numbers and status words. Flag cost or time only when their log already has that mark; otherwise say unknown and ask. Truncated question text points at the PDF, not a rewrite. Aging is a date compare they can correct, not a claim. The pack quotes the export they dropped and does not invent due dates from a five-day custom.

**How to run:** Follow `docs/role/work-item-method.md`. Use or create `work-items/<id>/`. Put source files in `in/`. For each YAML step below, in order: (1) do not start if `needs` files are missing — ask the operator; (2) read the `tool` file under `docs/tools/`; (3) write `produce_path` inside this Work Item folder (`work/` and `out/` are relative to the Work Item, not the expert root); (4) run `check` with those same relative paths; (5) on fail, retry at most 3 times then ask via **operator-qa**; (6) update the Work Item journal with **journal-keeper**. After the last step, the pack in `out/` must quote their source files. Do not invent counts, dates, approvals, or answers.

**Initial phase:** `intake`

## Work map

```yaml
id: rfi-status
steps:
  - id: pull
    needs: []
    produces: rfi-raw
    produce_path: work/rfi-log.csv
    tool: docs/tools/rfi-log.md
    check: python docs/tools/checks/csv-has-columns.py work/rfi-log.csv number status
    on_fail: retry
    next: [age]
  - id: age
    needs: [rfi-raw]
    produces: rfi-aged
    produce_path: work/rfi-aged.csv
    tool: docs/tools/rfi-log.md
    check: python docs/tools/checks/csv-has-columns.py work/rfi-aged.csv number status
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [rfi-aged]
    produces: rfi-pack
    produce_path: out/rfi-status.md
    tool: docs/tools/procore-pattern.md
    check: python docs/tools/checks/file-exists.py out/rfi-status.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they confirm how this shop files.
