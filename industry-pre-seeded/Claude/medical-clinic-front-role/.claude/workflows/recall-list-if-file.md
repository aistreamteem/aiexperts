# Recall List If File

**When to use:** If they exported a recall or reminder list, shape it: chart label, due date as stored, type as they labeled it. They send reminders. You do not message patients and you do not invent a due date from a generic annual habit. If they have no recall export, say the file is missing — do not build one from memory. Hours and holiday blocks still apply when they asked you to propose slots. Prefer chart number. Extra clinical notes stay out of docs/.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Follow this file's steps in order. Read the named tool doc, write artifacts under this Work Item's `work/` and `out/`, then run **journal-keeper**.

**Initial phase:** `role-job`

## Work map

```yaml
id: recall-list-if-file
steps:
  - id: pull
    needs: []
    produces: recall
    produce_path: work/recall.csv
    tool: docs/tools/ehr-export.md
    check: python docs/tools/checks/file-exists.py work/recall.csv
    on_fail: retry
    next: [columns]
  - id: columns
    needs: [recall]
    produces: recall-cols
    produce_path: work/recall.csv
    tool: docs/tools/ehr-export.md
    check: python docs/tools/checks/csv-has-columns.py work/recall.csv chart due
    on_fail: retry
    next: [write]
  - id: write
    needs: [recall-cols]
    produces: recall-writeup
    produce_path: out/recall.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/recall.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator confirms how this clinic files.
