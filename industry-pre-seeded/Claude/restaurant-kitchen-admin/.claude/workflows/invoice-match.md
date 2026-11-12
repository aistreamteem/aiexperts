# Invoice Match

**When to use:** Match the vendor invoice to the order and to receiving notes if they have them. Shorts, substitutions, price jumps off bid, wrong spec, and catch-weight gaps are questions. No payment, no invented credit amount, no silent price change on the guide. Do not call a two-way file a three-way match. Keep account secrets out of the folder. One pack is one ticket unless they asked to index a week. Alcohol lines still do not get license advice.

**How to run:** Self-contained. Active Work Item under `work-items/<id>/`. For each ready step: read the tool doc → write `produce_path` inside that Work Item → run the check with working directory = the Work Item folder → journal-keeper. One **continue** = one ready step unless they asked to finish this job.

**Initial phase:** `inv`

## Work map

```yaml
id: invoice-match
steps:
  - id: inv
    needs: []
    produces: inv-raw
    produce_path: work/invoice-lines.csv
    tool: docs/tools/invoice-pdf.md
    check: python docs/tools/checks/csv-has-columns.py work/invoice-lines.csv item qty price
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [inv-raw]
    produces: match-pack
    produce_path: out/invoice-match.md
    tool: docs/tools/receiving-log.md
    check: python docs/tools/checks/file-exists.py out/invoice-match.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator confirms how this kitchen files (`remember` / `integrate-docs`).
