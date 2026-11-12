# Pickup Notify List

**When to use:** From the lab-status or tray export, list jobs their status word says are ready and not yet marked notified. Chart label, job or tray number, preferred contact as stored. They call or text. You do not send the notice and you do not invent that someone was reached. Ready must come from their status file, not a guessed ship date. Do not include Rx powers on the notify list. Extra phones the list does not need stay out. Minors follow their guardian contact fields. Produce the list plus a pack note.

**How to run:** Select this job with **workflow-selector** (or name it). Keep artifacts under `work-items/<id>/`. Walk one ready step per **continue** unless they asked for the whole job. For each step: read the tool file, write `produce_path` inside the Work Item folder, run the check against that same path, store the log in `evidence/`, then **journal-keeper**. Do not start a step if its `needs` files are missing. On check fail, retry at most 3 times, then ask. If a required export is missing, ask; do not invent rows.

**Initial phase:** `intake`, then the first YAML step. Paths `work/` and `out/` mean inside the current Work Item.

## Work map

```yaml
id: pickup-notify-list
steps:
  - id: status
    needs: []
    produces: status
    produce_path: work/lab-status.csv
    tool: docs/tools/lab-status.md
    check: python docs/tools/checks/csv-has-columns.py work/lab-status.csv job status
    on_fail: retry
    next: [day]
  - id: day
    needs: [status]
    produces: day
    produce_path: work/day-list.csv
    tool: docs/tools/day-list-csv.md
    check: python docs/tools/checks/file-exists.py work/day-list.csv
    on_fail: retry
    next: [write]
  - id: write
    needs: [status, day]
    produces: notify-writeup
    produce_path: out/pickup-notify.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/pickup-notify.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this office via **remember**.
