# Bid Compare

**When to use:** Compare amounts, allowances, exclusions, and dates from bid PDFs they provided for one project. Do not pick a winner or lowest responsible bidder. Missing scope pages and vendors not on their insurance checklist are questions. Keep add-alternates labeled. One project per comparison write-up unless they asked for an index with a project column. Produce the CSV the checks can see, then the write-up.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put operator files in `in/`. Walk the YAML steps below in order (one ready step per **continue** unless the operator asked for the whole named job). For each step: read the cited tool doc under `docs/tools/`, write the produced file under this Work Item (`work/` or `out/`), run the listed check against those same paths, copy check logs to `evidence/`, then update the Work Item journal with **journal-keeper**. Do not start a step whose `needs` files are missing. On check fail, retry the same step at most three times, then record the blocker and ask the operator. Human gates in `docs/role/work-item-method.md` are not passed by the word continue.

**Initial phase:** `role-job`

## Work map

```yaml
id: bid-compare
steps:
  - id: index
    needs: []
    produces: bids-raw
    produce_path: work/bids.csv
    tool: docs/tools/bid-pdf.md
    check: python docs/tools/checks/file-exists.py work/bids.csv
    on_fail: retry
    next: [columns]
  - id: columns
    needs: [bids-raw]
    produces: bids-cols
    produce_path: work/bids.csv
    tool: docs/tools/bid-pdf.md
    check: python docs/tools/checks/csv-has-columns.py work/bids.csv vendor amount
    on_fail: retry
    next: [write]
  - id: write
    needs: [bids-cols]
    produces: bids-writeup
    produce_path: out/bid-compare.md
    tool: docs/tools/bid-pdf.md
    check: python docs/tools/checks/file-exists.py out/bid-compare.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator **remember**s how this shop actually files.
