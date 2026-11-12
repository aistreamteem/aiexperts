# EOB Index

**When to use:** Index EOB or ERA PDFs they saved: payer, claim label, amounts as printed. Do not say the allowed amount is correct. Do not infer paid from a clearinghouse acknowledgment alone. Do not change a code because the EOB downcoded a line. Keep billed, allowed, paid, and patient responsibility separate. Do not copy a full member SSN into the index. Secondary pages needed for coordination are present or missing. Pending stays pending if their file says so.

**How to run:** Open or reuse `work-items/<id>/`. Put the source export in `in/`. Follow this map in order: read the named `docs/tools/` file, write `produce_path` inside this Work Item, run the step `check`, retry at most 3 times on fail then ask. Pass produced files to the next step. One ready step per continue unless the operator asked for the whole job. Then journal-keeper.

**Initial phase:** `role-job`

## Work map

```yaml
id: eob-index
steps:
  - id: index
    needs: []
    produces: eob-raw
    produce_path: work/eob-index.csv
    tool: docs/tools/eob-pdf.md
    check: python docs/tools/checks/file-exists.py work/eob-index.csv
    on_fail: retry
    next: [columns]
  - id: columns
    needs: [eob-raw]
    produces: eob-cols
    produce_path: work/eob-index.csv
    tool: docs/tools/eob-pdf.md
    check: python docs/tools/checks/csv-has-columns.py work/eob-index.csv file status
    on_fail: retry
    next: [write]
  - id: write
    needs: [eob-cols]
    produces: eob-writeup
    produce_path: out/eob-index.md
    tool: docs/tools/eob-pdf.md
    check: python docs/tools/checks/file-exists.py out/eob-index.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator confirms how this office works.
