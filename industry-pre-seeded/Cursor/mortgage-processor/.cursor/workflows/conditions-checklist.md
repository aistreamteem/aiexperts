# Conditions checklist

**When to use:** Build a conditions checklist from their conditions sheet: loan number, condition text, PTD/PTF/suspense as they coded it, and status. Attach present-missing only when the matching document is in the pack. Do not invent a condition. Do not mark cleared without their code. Do not declare CTC. Do not underwrite. Write-up names which rows came from their export versus a guess you labeled.

**How to run:** Open or continue a Work Item under `work-items/<id>/` using `continue` and `workflow-selector`. Copy `work-items/_TEMPLATE/` if the folder does not exist. Put source files in `in/`. Follow the steps below in order. Read each step's tool file under `docs/tools/`. Write artifacts at the YAML `produce_path` relative to the Work Item root (`work/` then `out/`). Run the step `check` from the Work Item root. Do not start a step whose `needs` files are missing. On check fail, retry at most three times, then ask with `operator-qa`. After each step, update the Work Item journal with `journal-keeper`. Human gate: label guesses; never declare CTC or a lock from a completed checklist. Completeness is not a lending decision.

**Initial phase:** `role-job`

## Work map

```yaml
id: conditions-checklist
steps:
  - id: sheet
    needs: []
    produces: conditions
    produce_path: work/conditions.csv
    tool: docs/tools/conditions-sheet.md
    check: python docs/tools/checks/csv-has-columns.py work/conditions.csv loan condition
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [conditions]
    produces: checklist
    produce_path: out/conditions-checklist.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/conditions-checklist.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects how *this* shop files.
