# Loan File Index

**When to use:** Open a loan by indexing PDFs they stored: application, identification (minimum necessary), income docs, asset docs, VOE, purchase contract, and other imaged items as present versus missing. Do not underwrite. Do not copy a full SSN or a credit score into the index. Do not treat a pre-qual worksheet as the application. Do not invent a document type. The pack is an intake index, not an approval.

**How to run:** Open or continue a Work Item under `work-items/<id>/` using `continue` and `workflow-selector`. Copy `work-items/_TEMPLATE/` if the folder does not exist. Put source files in `in/`. Follow the steps below in order. Read each step's tool file under `docs/tools/`. Write artifacts at the YAML `produce_path` relative to the Work Item root (`work/` then `out/`). Run the step `check` from the Work Item root. Do not start a step whose `needs` files are missing. On check fail, retry at most three times, then ask with `operator-qa`. After each step, update the Work Item journal with `journal-keeper`. Human gate: label guesses; never declare CTC or a lock from a completed checklist. Completeness is not a lending decision.

**Initial phase:** `role-job`

## Work map

```yaml
id: loan-file-index
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
    produces: file-index
    produce_path: out/loan-file-index.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/loan-file-index.md
    on_fail: retry
    next: []
```

Replace tools and checks when the operator corrects how *this* shop files.
