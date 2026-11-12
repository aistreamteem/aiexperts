# Bank Review

**When to use:** From a bank CSV they export for one account and date range, list unclear lines, possible transfers, owner deposits, and processor names that are not the real payee. Produce raw lines, a flagged sheet with a question column, and a write-up. Do not invent payees because an amount looks like rent. Transfers and owner deposits stay questions until they teach. Do not treat a 90-day download as a month unless they named that range. No bank login. No full account numbers in the write-up. The next decision is their answers, then coding or the rec, not a silent recode.

**How to run:** Select this job with workflow-selector (or continue). Use `work-items/<id>/`. Put source files in `in/`. Walk one ready step: read the named tool doc, write the produced file under this Work Item, run the check, then journal-keeper. Do not skip a step with a chat summary. Whole named job only if they asked.

**Initial phase:** `role-job`

## Work map

```yaml
id: bank-review
steps:
  - id: import
    needs: []
    produces: bank-raw
    produce_path: work/bank-raw.csv
    tool: docs/tools/bank-csv.md
    check: python docs/tools/checks/file-exists.py work/bank-raw.csv
    on_fail: retry
    next: [flag]
  - id: flag
    needs: [bank-raw]
    produces: bank-flagged
    produce_path: work/bank-flagged.csv
    tool: docs/tools/bank-csv.md
    check: python docs/tools/checks/csv-has-columns.py work/bank-flagged.csv date amount question
    on_fail: retry
    next: [writeup]
  - id: writeup
    needs: [bank-flagged]
    produces: bank-questions
    produce_path: out/bank-questions.md
    tool: docs/tools/bank-csv.md
    check: python docs/tools/checks/file-exists.py out/bank-questions.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator confirms how this shop works.
