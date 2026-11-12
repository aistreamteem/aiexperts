# Ratio From Their Posted

**When to use:** Compare children present from attendance to staff on their schedule using only the posted ratio or maximum they wrote for that room. Show the two counts and their posted number. Do not invent a state statute and do not declare the room legal or illegal. Do not move children or staff on paper to tidy the math. Missing staff-count data is an ask. Mixed-age rooms use their mixed-age note if they have one. Alerts go to the director. You never release a child to fix a number.

**How to run:** Self-contained. Confirm an active Work Item at `work-items/<id>/` (copy `work-items/_TEMPLATE/` if needed). Paths `in/`, `work/`, `out/`, and `evidence/` are inside that folder. Load operations memory, then walk the map: a step is ready when every `needs` artifact exists on disk. Read the named `docs/tools/` file, produce `produce_path`, run `check` from the Work Item folder. On fail, retry at most 3 times, then ask with **operator-qa**. Do not invent a pass. After each step, **journal-keeper**. One ready step per **continue** unless the operator asked for the whole job. Finished pack lands in `out/`. Director gates (start, release, signatures) are not skipped.

**Initial phase:** `role-job`

## Work map

```yaml
id: ratio-from-their-posted
steps:
  - id: roster
    needs: []
    produces: roster
    produce_path: work/roster.csv
    tool: docs/tools/roster-sheet.md
    check: python docs/tools/checks/csv-has-columns.py work/roster.csv child room
    on_fail: retry
    next: [att]
  - id: att
    needs: [roster]
    produces: att
    produce_path: work/attendance.csv
    tool: docs/tools/attendance-csv.md
    check: python docs/tools/checks/csv-has-columns.py work/attendance.csv child status
    on_fail: retry
    next: [write]
  - id: write
    needs: [roster, att]
    produces: ratio-pack
    produce_path: out/ratio-from-posted.md
    tool: docs/tools/roster-sheet.md
    check: python docs/tools/checks/file-exists.py out/ratio-from-posted.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects them through **remember**.
