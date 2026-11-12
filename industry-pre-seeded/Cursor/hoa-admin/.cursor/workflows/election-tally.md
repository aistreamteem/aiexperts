# Election Tally

**When to use:** Count from the roster and ballot or proxy files they provide. Label the product a tally, not a certified election. List missing signatures and unmarked choices as questions. Do not rule on proxy validity or announce a legal winner. Do not publish how a named lot voted. One meeting and one association per tally. Produce the CSV the checks can see, then the write-up.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put operator files in `in/`. Walk the YAML steps below in order (one ready step per **continue** unless the operator asked for the whole named job). For each step: read the cited tool doc under `docs/tools/`, write the produced file under this Work Item (`work/` or `out/`), run the listed check against those same paths, copy check logs to `evidence/`, then update the Work Item journal with **journal-keeper**. Do not start a step whose `needs` files are missing. On check fail, retry the same step at most three times, then record the blocker and ask the operator. Human gates in `docs/role/work-item-method.md` are not passed by the word continue.

**Initial phase:** `role-job`

## Work map

```yaml
id: election-tally
steps:
  - id: roster
    needs: []
    produces: roster
    produce_path: work/roster.csv
    tool: docs/tools/roster-csv.md
    check: python docs/tools/checks/file-exists.py work/roster.csv
    on_fail: retry
    next: [tally]
  - id: tally
    needs: [roster]
    produces: tally-raw
    produce_path: work/election-tally.csv
    tool: docs/tools/roster-csv.md
    check: python docs/tools/checks/csv-has-columns.py work/election-tally.csv candidate votes
    on_fail: retry
    next: [write]
  - id: write
    needs: [tally-raw]
    produces: tally-writeup
    produce_path: out/election-tally.md
    tool: docs/tools/roster-csv.md
    check: python docs/tools/checks/file-exists.py out/election-tally.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator **remember**s how this shop actually files.
