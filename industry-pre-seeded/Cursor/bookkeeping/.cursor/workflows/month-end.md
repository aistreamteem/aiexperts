# Month End

**When to use:** Close notes for one period they name: gather inputs, record rec status per account, list open questions, and write a short close pack. Accruals only if they already use them. Do not call the month filed, audited, or closed if a rec is open and they did not accept it. Do not mix two months. Do not hide plugs in a clean profit and loss. Ask what locked means here. Produce the input list, rec status CSV, questions CSV, and out/month-end.md. They or their CPA decide whether books are done enough for the CPA pack. Starter close list is a guess until they teach their checklist.

**How to run:** Select this job with workflow-selector (or continue). Use `work-items/<id>/`. Put source files in `in/`. Walk one ready step: read the named tool doc, write the produced file under this Work Item, run the check, then journal-keeper. Do not skip a step with a chat summary. Whole named job only if they asked.

**Initial phase:** `role-job`

## Work map

```yaml
id: month-end
steps:
  - id: gather
    needs: []
    produces: close-inputs
    produce_path: work/close-inputs.csv
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py work/close-inputs.csv
    on_fail: retry
    next: [rec-check]
  - id: rec-check
    needs: [close-inputs]
    produces: close-rec-status
    produce_path: work/close-rec-status.csv
    tool: docs/tools/reconcile-pack.md
    check: python docs/tools/checks/csv-has-columns.py work/close-rec-status.csv account status
    on_fail: retry
    next: [questions, close-notes]
  - id: questions
    needs: [close-rec-status]
    produces: close-questions
    produce_path: work/close-questions.csv
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py work/close-questions.csv
    on_fail: retry
    next: [close-notes]
  - id: close-notes
    needs: [close-rec-status, close-questions]
    produces: month-end-pack
    produce_path: out/month-end.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/month-end.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator confirms how this shop works.
