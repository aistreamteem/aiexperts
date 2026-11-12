# Board Files

**When to use:** Assemble a present-or-missing list of files for the next meeting they name: agenda, last approved minutes, financials they already produced, and exhibits they listed. They run the meeting. Minutes stay actions, not a transcript. Keep collections detail out of the open pack unless their template separates it. One meeting date and one association per index. Produce the CSV the checks can see, then the write-up.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put operator files in `in/`. Walk the YAML steps below in order (one ready step per **continue** unless the operator asked for the whole named job). For each step: read the cited tool doc under `docs/tools/`, write the produced file under this Work Item (`work/` or `out/`), run the listed check against those same paths, copy check logs to `evidence/`, then update the Work Item journal with **journal-keeper**. Do not start a step whose `needs` files are missing. On check fail, retry the same step at most three times, then record the blocker and ask the operator. Human gates in `docs/role/work-item-method.md` are not passed by the word continue.

**Initial phase:** `role-job`

## Work map

```yaml
id: board-files
steps:
  - id: list
    needs: []
    produces: board-index
    produce_path: work/board-files.csv
    tool: docs/tools/board-folder.md
    check: python docs/tools/checks/file-exists.py work/board-files.csv
    on_fail: retry
    next: [columns]
  - id: columns
    needs: [board-index]
    produces: board-cols
    produce_path: work/board-files.csv
    tool: docs/tools/board-folder.md
    check: python docs/tools/checks/csv-has-columns.py work/board-files.csv file present
    on_fail: retry
    next: [write]
  - id: write
    needs: [board-cols]
    produces: board-writeup
    produce_path: out/board-files.md
    tool: docs/tools/board-folder.md
    check: python docs/tools/checks/file-exists.py out/board-files.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator **remember**s how this shop actually files.
