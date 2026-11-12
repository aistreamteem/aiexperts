# Holiday Calendar Pack

**When to use:** Copy the year’s closures, staff-only days, and tuition-charged holidays from their calendar file and quote the handbook exhibit when the calendar is silent on whether tuition is due. Do not invent a federal-holiday rule. Camp weeks and school-district days off stay labeled if they split those calendars. Confirm the year on the file. They send parent notices unless they taught a send step. If two calendars disagree, quote both. Extra-care does not run on a closed day unless their file says so.

**How to run:** Self-contained. Confirm an active Work Item at `work-items/<id>/` (copy `work-items/_TEMPLATE/` if needed). Paths `in/`, `work/`, `out/`, and `evidence/` are inside that folder. Load operations memory, then walk the map: a step is ready when every `needs` artifact exists on disk. Read the named `docs/tools/` file, produce `produce_path`, run `check` from the Work Item folder. On fail, retry at most 3 times, then ask with **operator-qa**. Do not invent a pass. After each step, **journal-keeper**. One ready step per **continue** unless the operator asked for the whole job. Finished pack lands in `out/`. Director gates (start, release, signatures) are not skipped.

**Initial phase:** `role-job`

## Work map

```yaml
id: holiday-calendar-pack
steps:
  - id: cal
    needs: []
    produces: cal
    produce_path: work/calendar.csv
    tool: docs/tools/calendar-file.md
    check: python docs/tools/checks/file-exists.py work/calendar.csv
    on_fail: retry
    next: [handbook]
  - id: handbook
    needs: [cal]
    produces: handbook
    produce_path: work/handbook-notes.csv
    tool: docs/tools/handbook-pdf.md
    check: python docs/tools/checks/file-exists.py work/handbook-notes.csv
    on_fail: retry
    next: [write]
  - id: write
    needs: [cal, handbook]
    produces: cal-pack
    produce_path: out/holiday-calendar.md
    tool: docs/tools/calendar-file.md
    check: python docs/tools/checks/file-exists.py out/holiday-calendar.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects them through **remember**.
