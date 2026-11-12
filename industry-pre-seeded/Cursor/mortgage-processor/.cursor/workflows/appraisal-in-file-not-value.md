# Appraisal in file (not a value)

**When to use:** Index the appraisal PDF folder: report present, report date, invoice, AOA, and printed appraisal conditions as text. Do not give a value opinion. Do not invent a value. Do not compare to a CMA. Do not pay the AMC. Ordered-but-missing stays missing, not a denial. Do not treat a completion photo as a value you certify. Write-up is a file pack, not an underwrite of collateral.

**How to run:** Open or continue a Work Item under `work-items/<id>/` using `continue` and `workflow-selector`. Copy `work-items/_TEMPLATE/` if the folder does not exist. Put source files in `in/`. Follow the steps below in order. Read each step's tool file under `docs/tools/`. Write artifacts at the YAML `produce_path` relative to the Work Item root (`work/` then `out/`). Run the step `check` from the Work Item root. Do not start a step whose `needs` files are missing. On check fail, retry at most three times, then ask with `operator-qa`. After each step, update the Work Item journal with `journal-keeper`. Human gate: label guesses; never declare CTC or a lock from a completed checklist. Completeness is not a lending decision.

**Initial phase:** `role-job`

## Work map

```yaml
id: appraisal-in-file-not-value
steps:
  - id: appr
    needs: []
    produces: appraisal
    produce_path: work/appraisal-index.csv
    tool: docs/tools/appraisal-pdf-folder.md
    check: python docs/tools/checks/csv-has-columns.py work/appraisal-index.csv loan document
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [appraisal]
    produces: appraisal-pack
    produce_path: out/appraisal-in-file.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/appraisal-in-file.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects how *this* shop files.
