# Suspense List As Their Codes

**When to use:** List suspense and rereq items from their conditions sheet using their codes and comments only. Do not translate a code into a denial or an easy fix. Do not unsuspend. Do not invent a reason. Do not approve. Do not invent a rate to “fix” suspense. Write-up is their status plus dated evidence rows, not a prognosis and not a fair-lending opinion.

**How to run:** Open or continue a Work Item under `work-items/<id>/` using `continue` and `workflow-selector`. Copy `work-items/_TEMPLATE/` if the folder does not exist. Put source files in `in/`. Follow the steps below in order. Read each step's tool file under `docs/tools/`. Write artifacts at the YAML `produce_path` relative to the Work Item root (`work/` then `out/`). Run the step `check` from the Work Item root. Do not start a step whose `needs` files are missing. On check fail, retry at most three times, then ask with `operator-qa`. After each step, update the Work Item journal with `journal-keeper`. Human gate: label guesses; never declare CTC or a lock from a completed checklist. Completeness is not a lending decision.

**Initial phase:** `role-job`

## Work map

```yaml
id: suspense-list-as-their-codes
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
    produces: suspense-pack
    produce_path: out/suspense-list.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/suspense-list.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects how *this* shop files.
