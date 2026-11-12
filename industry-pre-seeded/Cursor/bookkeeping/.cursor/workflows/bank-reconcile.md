# Bank Reconcile

**When to use:** Match one statement they named to the books for that account and period. Build statement lines, list outstanding checks and deposits-in-transit with status, and write a rec pack that shows the difference. Do not plug miscellaneous income or expense to force a zero. They confirm matched. Ask the cutoff for old uncleared items. Do not call the month closed if the rec is open and they did not accept the difference. Pointer to their software rec page only; no login. Save the worksheet with the statement PDF they provided. Starter outstanding items come only from their files, not from invented checks.

**How to run:** Select this job with workflow-selector (or continue). Use `work-items/<id>/`. Put source files in `in/`. Walk one ready step: read the named tool doc, write the produced file under this Work Item, run the check, then journal-keeper. Do not skip a step with a chat summary. Whole named job only if they asked.

**Initial phase:** `role-job`

## Work map

```yaml
id: bank-reconcile
steps:
  - id: statement
    needs: []
    produces: rec-statement
    produce_path: work/bank-statement-lines.csv
    tool: docs/tools/reconcile-pack.md
    check: python docs/tools/checks/file-exists.py work/bank-statement-lines.csv
    on_fail: retry
    next: [match]
  - id: match
    needs: [rec-statement]
    produces: rec-outstanding
    produce_path: work/bank-outstanding.csv
    tool: docs/tools/reconcile-pack.md
    check: python docs/tools/checks/csv-has-columns.py work/bank-outstanding.csv date amount status
    on_fail: retry
    next: [rec-writeup]
  - id: rec-writeup
    needs: [rec-outstanding]
    produces: rec-pack
    produce_path: out/bank-reconcile.md
    tool: docs/tools/reconcile-pack.md
    check: python docs/tools/checks/file-exists.py out/bank-reconcile.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator confirms how this shop works.
