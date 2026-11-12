# Tuition From File

**When to use:** Build a tuition or past-due list only from their rate sheet and ledger export. Quote the rate that matches the child’s schedule on the contract. Do not invent a weekly number, sibling percent, or late fee. You never send money or store a card. Subsidy copays stay on the authorization file if they split them. NSF rows keep their code. Year-end paid totals use the paid column only. If contract and rate sheet disagree, quote both and ask.

**How to run:** Self-contained. Confirm an active Work Item at `work-items/<id>/` (copy `work-items/_TEMPLATE/` if needed). Paths `in/`, `work/`, `out/`, and `evidence/` are inside that folder. Load operations memory, then walk the map: a step is ready when every `needs` artifact exists on disk. Read the named `docs/tools/` file, produce `produce_path`, run `check` from the Work Item folder. On fail, retry at most 3 times, then ask with **operator-qa**. Do not invent a pass. After each step, **journal-keeper**. One ready step per **continue** unless the operator asked for the whole job. Finished pack lands in `out/`. Director gates (start, release, signatures) are not skipped.

**Initial phase:** `role-job`

## Work map

```yaml
id: tuition-from-file
steps:
  - id: rates
    needs: []
    produces: rates
    produce_path: work/tuition.csv
    tool: docs/tools/tuition-sheet.md
    check: python docs/tools/checks/csv-has-columns.py work/tuition.csv child rate
    on_fail: retry
    next: [grid]
  - id: grid
    needs: [rates]
    produces: grid
    produce_path: work/tuition-list.csv
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py work/tuition-list.csv
    on_fail: retry
    next: [write]
  - id: write
    needs: [rates, grid]
    produces: tuition-pack
    produce_path: out/tuition-from-file.md
    tool: docs/tools/tuition-sheet.md
    check: python docs/tools/checks/file-exists.py out/tuition-from-file.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects them through **remember**.
