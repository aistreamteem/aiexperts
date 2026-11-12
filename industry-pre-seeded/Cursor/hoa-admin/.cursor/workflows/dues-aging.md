# Dues Aging

**When to use:** List balances by current, thirty, sixty, and ninety-plus from their ledger export after you confirm community name and as-of date. No demand letter, no lien threat, no credit-reporting language. Late-fee math only if their policy file states the formula and they asked for arithmetic. Prepaid lots are not delinquent. One association per aging file. Produce the CSV the checks can see, then the write-up.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put operator files in `in/`. Walk the YAML steps below in order (one ready step per **continue** unless the operator asked for the whole named job). For each step: read the cited tool doc under `docs/tools/`, write the produced file under this Work Item (`work/` or `out/`), run the listed check against those same paths, copy check logs to `evidence/`, then update the Work Item journal with **journal-keeper**. Do not start a step whose `needs` files are missing. On check fail, retry the same step at most three times, then record the blocker and ask the operator. Human gates in `docs/role/work-item-method.md` are not passed by the word continue.

**Initial phase:** `role-job`

## Work map

```yaml
id: dues-aging
steps:
  - id: pull
    needs: []
    produces: dues-raw
    produce_path: work/dues-aging.csv
    tool: docs/tools/ledger-export.md
    check: python docs/tools/checks/file-exists.py work/dues-aging.csv
    on_fail: retry
    next: [columns]
  - id: columns
    needs: [dues-raw]
    produces: dues-cols
    produce_path: work/dues-aging.csv
    tool: docs/tools/ledger-export.md
    check: python docs/tools/checks/csv-has-columns.py work/dues-aging.csv lot balance
    on_fail: retry
    next: [write]
  - id: write
    needs: [dues-cols]
    produces: dues-writeup
    produce_path: out/dues-aging.md
    tool: docs/tools/ledger-export.md
    check: python docs/tools/checks/file-exists.py out/dues-aging.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator **remember**s how this shop actually files.
