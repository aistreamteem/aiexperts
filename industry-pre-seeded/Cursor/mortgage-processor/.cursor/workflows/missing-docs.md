# Missing-docs list

**When to use:** Compare their document-folder index to the conditions sheet and list named items that are missing, cut off, or undated. Do not invent a document type. Do not copy a full SSN or a credit score into the list. Do not treat missing as a denial. Income, VOE, contract, and title rows stay typed as they typed them. Write-up is a missing list plus asks, not an underwrite.

**How to run:** Open or continue a Work Item under `work-items/<id>/` using `continue` and `workflow-selector`. Copy `work-items/_TEMPLATE/` if the folder does not exist. Put source files in `in/`. Follow the steps below in order. Read each step's tool file under `docs/tools/`. Write artifacts at the YAML `produce_path` relative to the Work Item root (`work/` then `out/`). Run the step `check` from the Work Item root. Do not start a step whose `needs` files are missing. On check fail, retry at most three times, then ask with `operator-qa`. After each step, update the Work Item journal with `journal-keeper`. Human gate: label guesses; never declare CTC or a lock from a completed checklist. Completeness is not a lending decision.

**Initial phase:** `role-job`

## Work map

```yaml
id: missing-docs
steps:
  - id: index
    needs: []
    produces: index
    produce_path: work/document-index.csv
    tool: docs/tools/document-folder-index.md
    check: python docs/tools/checks/csv-has-columns.py work/document-index.csv loan document
    on_fail: retry
    next: [conds]
  - id: conds
    needs: [index]
    produces: conditions
    produce_path: work/conditions.csv
    tool: docs/tools/conditions-sheet.md
    check: python docs/tools/checks/file-exists.py work/conditions.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [index, conditions]
    produces: missing
    produce_path: out/missing-docs.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/missing-docs.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects how *this* shop files.
