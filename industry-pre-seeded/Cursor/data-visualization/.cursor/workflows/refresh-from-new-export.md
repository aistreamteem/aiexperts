# Refresh from a new export

**When to use:** Read a new CSV with the same columns they already named. Write a dated PNG and a write-up that compares old file name versus new file name, row counts, and date ranges — not growth you invented. If columns changed, stop and ask. Do not scrape. Keep the prior PNG unless they said replace. Same filters as last pack. Version the source names in the markdown.

**Initial phase:** `question`

**Method:** `docs/role/work-item-method.md` — review / refresh cycle.

## How to run

This file is self-contained. Walk it with **continue** / **journal-keeper**.

1. Confirm an active Work Item under `work-items/<id>/` (new dated folder, or dated files if they said to replace in place). Paths below are **inside that folder**.
2. **Question gate:** same question and columns as the prior pack; they named the new file. If columns changed, stop and ask.
3. Put the new export in `in/`. Load `docs/tools/csv-folder.md` and `docs/tools/matplotlib.md`. Name both source versions in the write-up.
4. Do one ready step per continue unless they asked for the whole job.
5. For each step: produce the file, run the check from the Work Item folder, log under `evidence/`. Retry at most three times, then ask.
6. **journal-keeper** after the step.

## Work map

```yaml
id: refresh-from-new-export
steps:
  - id: newfile
    needs: []
    produces: newfile
    produce_path: work/refresh-new.csv
    tool: docs/tools/csv-folder.md
    check: python docs/tools/checks/file-exists.py work/refresh-new.csv
    on_fail: retry
    next: [chart]
  - id: chart
    needs: [newfile]
    produces: png
    produce_path: out/refresh-dated.png
    tool: docs/tools/matplotlib.md
    check: python docs/tools/checks/file-exists.py out/refresh-dated.png
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [png]
    produces: writeup
    produce_path: out/refresh-from-new-export.md
    tool: docs/tools/python.md
    check: python docs/tools/checks/file-exists.py out/refresh-from-new-export.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they teach.
