# Recall List

**When to use:** If they exported a recall or reminder list, shape it: chart label, due date as stored, type as they labeled it. They send reminders. You do not message patients and you do not invent a due date from a generic annual habit. You do not say the patient is clinically due. Contact-lens check types stay as they labeled them, not a fit you schedule as the doctor. If they have no recall export, say the file is missing. Hours and holiday blocks still apply when they asked you to propose slots. Prefer chart number. Extra clinical notes stay out of docs/.

**How to run:** Select this job with **workflow-selector** (or name it). Keep artifacts under `work-items/<id>/`. Walk one ready step per **continue** unless they asked for the whole job. For each step: read the tool file, write `produce_path` inside the Work Item folder, run the check against that same path, store the log in `evidence/`, then **journal-keeper**. Do not start a step if its `needs` files are missing. On check fail, retry at most 3 times, then ask. If a required export is missing, ask; do not invent rows.

**Initial phase:** `intake`, then the first YAML step. Paths `work/` and `out/` mean inside the current Work Item.

## Work map

```yaml
id: recall-list
steps:
  - id: pull
    needs: []
    produces: recall
    produce_path: work/recall.csv
    tool: docs/tools/recall-csv.md
    check: python docs/tools/checks/file-exists.py work/recall.csv
    on_fail: retry
    next: [columns]
  - id: columns
    needs: [recall]
    produces: recall-cols
    produce_path: work/recall.csv
    tool: docs/tools/recall-csv.md
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

Starter work map. Replace tools and checks when they correct this office via **remember**.
