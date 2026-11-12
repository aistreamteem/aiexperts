# Reserve Index

**When to use:** Confirm the reserve-study PDF is present, copy the report date and association name on the cover, and copy any printed number they asked for. Not an engineering restamp and not a cash transfer. A missing or unexpectedly old study is a question for the board. One association per index. Produce the CSV the checks can see, then the write-up. Do not add or delete components, and do not move operating cash into reserves.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put operator files in `in/`. Walk the YAML steps below in order (one ready step per **continue** unless the operator asked for the whole named job). For each step: read the cited tool doc under `docs/tools/`, write the produced file under this Work Item (`work/` or `out/`), run the listed check against those same paths, copy check logs to `evidence/`, then update the Work Item journal with **journal-keeper**. Do not start a step whose `needs` files are missing. On check fail, retry the same step at most three times, then record the blocker and ask the operator. Human gates in `docs/role/work-item-method.md` are not passed by the word continue.

**Initial phase:** `role-job`

## Work map

```yaml
id: reserve-index
steps:
  - id: index
    needs: []
    produces: rs-raw
    produce_path: work/reserve-index.csv
    tool: docs/tools/reserve-study-pdf.md
    check: python docs/tools/checks/file-exists.py work/reserve-index.csv
    on_fail: retry
    next: [write]
  - id: write
    needs: [rs-raw]
    produces: rs-writeup
    produce_path: out/reserve-index.md
    tool: docs/tools/reserve-study-pdf.md
    check: python docs/tools/checks/file-exists.py out/reserve-index.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator **remember**s how this shop actually files.
