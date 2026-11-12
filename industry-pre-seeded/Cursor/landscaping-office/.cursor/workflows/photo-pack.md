# Photo Pack

**When to use:** Index photos they stored to ticket and property. Keep or propose names that match their rule. Do not invent a shot or crop away a defect. Proposal photos stay with the estimate draft; after photos stay with closeout or callbacks. Min-necessary on faces and plates. Photos are not a disease label. They shoot again if a view is missing. You write the index and write-up the check can see.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Follow this file's steps in order. Read the cited tool doc, write artifacts under that Work Item's `work/` and `out/`, run the listed check against those same paths, then **journal-keeper**. Do not invent a missing ticket, price, or weather call — ask with **operator-qa**.

**Initial phase:** `role-job`

## Work map

```yaml
id: photo-pack
steps:
  - id: photos
    needs: []
    produces: photos
    produce_path: work/photo-index.csv
    tool: docs/tools/photo-folder.md
    check: python docs/tools/checks/file-exists.py work/photo-index.csv
    on_fail: retry
    next: [tickets]
  - id: tickets
    needs: [photos]
    produces: tickets
    produce_path: work/photo-tickets.csv
    tool: docs/tools/job-ticket-sheet.md
    check: python docs/tools/checks/file-exists.py work/photo-tickets.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [photos, tickets]
    produces: photo-pack
    produce_path: out/photo-pack.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/photo-pack.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct shop practice (**remember** / **integrate-docs**).

