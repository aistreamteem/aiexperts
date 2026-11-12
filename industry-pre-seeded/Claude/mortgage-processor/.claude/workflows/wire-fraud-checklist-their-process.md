# Wire Fraud Checklist Their Process

**When to use:** From their document index and working sheet, list whether their written wire-fraud or callback checklist rows are marked as they marked them. Do not send a wire. Do not republish wiring instructions or account numbers. Do not move funds. FBI and FTC pages are orientation only. Write-up is present-missing of their process rows, not a new instruction set. They verify. You list.

**How to run:** Open or continue a Work Item under `work-items/<id>/` using `continue` and `workflow-selector`. Copy `work-items/_TEMPLATE/` if the folder does not exist. Put source files in `in/`. Follow the steps below in order. Read each step's tool file under `docs/tools/`. Write artifacts at the YAML `produce_path` relative to the Work Item root (`work/` then `out/`). Run the step `check` from the Work Item root. Do not start a step whose `needs` files are missing. On check fail, retry at most three times, then ask with `operator-qa`. After each step, update the Work Item journal with `journal-keeper`. Human gate: label guesses; never declare CTC or a lock from a completed checklist. Completeness is not a lending decision.

**Initial phase:** `role-job`

## Work map

```yaml
id: wire-fraud-checklist-their-process
steps:
  - id: index
    needs: []
    produces: index
    produce_path: work/document-index.csv
    tool: docs/tools/document-folder-index.md
    check: python docs/tools/checks/csv-has-columns.py work/document-index.csv loan document
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [index]
    produces: wire-pack
    produce_path: out/wire-fraud-checklist.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/wire-fraud-checklist.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects how *this* shop files.
