# Day attendance list

**When to use:** From the attendance export, list the program date by room, child label they allow, and present/absent or in/out as they coded it. Confirm the file date before you treat it as today. Do not mark anyone present to tidy ratio. Flag sign-in gaps and illness wording as their words, not a diagnosis. Prefer child ID. Never release a child from this list. If roster and attendance disagree on who is enrolled versus present, quote both in the write-up.

**How to run:** Self-contained. Confirm an active Work Item at `work-items/<id>/` (copy `work-items/_TEMPLATE/` if needed). Paths `in/`, `work/`, `out/`, and `evidence/` are inside that folder. Load operations memory, then walk the map: a step is ready when every `needs` artifact exists on disk. Read the named `docs/tools/` file, produce `produce_path`, run `check` from the Work Item folder. On fail, retry at most 3 times, then ask with **operator-qa**. Do not invent a pass. After each step, **journal-keeper**. One ready step per **continue** unless the operator asked for the whole job. Finished pack lands in `out/`. Director gates (start, release, signatures) are not skipped.

**Initial phase:** `role-job`

## Work map

```yaml
id: attendance-day
steps:
  - id: pull
    needs: []
    produces: att
    produce_path: work/attendance.csv
    tool: docs/tools/attendance-csv.md
    check: python docs/tools/checks/csv-has-columns.py work/attendance.csv child status
    on_fail: retry
    next: [roster]
  - id: roster
    needs: [att]
    produces: roster
    produce_path: work/roster.csv
    tool: docs/tools/roster-sheet.md
    check: python docs/tools/checks/csv-has-columns.py work/roster.csv child room
    on_fail: retry
    next: [write]
  - id: write
    needs: [att, roster]
    produces: att-pack
    produce_path: out/attendance-day.md
    tool: docs/tools/attendance-csv.md
    check: python docs/tools/checks/file-exists.py out/attendance-day.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects them through **remember**.
