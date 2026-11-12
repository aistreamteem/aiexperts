# Material Pull

**When to use:** Build a pull list from sold tickets and their material sheet. Label qty by ticket when two jobs share a trailer. Do not invent yards or a chemical mix. Substitutes stay questions. Dump-trailer needs are an ask if not on the file. They buy and they load. You write the list and a write-up the check can see. Missing tickets stay holes, not guessed SKUs.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Follow this file's steps in order. Read the cited tool doc, write artifacts under that Work Item's `work/` and `out/`, run the listed check against those same paths, then **journal-keeper**. Do not invent a missing ticket, price, or weather call — ask with **operator-qa**.

**Initial phase:** `role-job`

## Work map

```yaml
id: material-pull
steps:
  - id: tickets
    needs: []
    produces: tickets
    produce_path: work/tickets.csv
    tool: docs/tools/job-ticket-sheet.md
    check: python docs/tools/checks/csv-has-columns.py work/tickets.csv ticket property service
    on_fail: retry
    next: [mats]
  - id: mats
    needs: [tickets]
    produces: mats
    produce_path: work/materials.csv
    tool: docs/tools/material-sheet.md
    check: python docs/tools/checks/csv-has-columns.py work/materials.csv sku qty
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [tickets, mats]
    produces: pull-pack
    produce_path: out/material-pull.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/material-pull.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct shop practice (**remember** / **integrate-docs**).
