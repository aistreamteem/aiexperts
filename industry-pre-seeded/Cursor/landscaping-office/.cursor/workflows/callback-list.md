# Callback List

**When to use:** List open callbacks from tickets they coded as return or complaint. Attach named photos if present. Do not diagnose turf or trees. Do not promise survival. Warranty versus courtesy versus billable follows their file. Hours come from their sheet, not invented time. Skip and dog flags still apply. They schedule the return. You write the list and questions, not a customer apology as if you were the owner.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Follow this file's steps in order. Read the cited tool doc, write artifacts under that Work Item's `work/` and `out/`, run the listed check against those same paths, then **journal-keeper**. Do not invent a missing ticket, price, or weather call — ask with **operator-qa**.

**Initial phase:** `role-job`

## Work map

```yaml
id: callback-list
steps:
  - id: tickets
    needs: []
    produces: tickets
    produce_path: work/callback-tickets.csv
    tool: docs/tools/job-ticket-sheet.md
    check: python docs/tools/checks/csv-has-columns.py work/callback-tickets.csv ticket property service
    on_fail: retry
    next: [photos]
  - id: photos
    needs: [tickets]
    produces: photos
    produce_path: work/photo-index.csv
    tool: docs/tools/photo-folder.md
    check: python docs/tools/checks/file-exists.py work/photo-index.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [tickets, photos]
    produces: callback-pack
    produce_path: out/callbacks.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/callbacks.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct shop practice (**remember** / **integrate-docs**).

