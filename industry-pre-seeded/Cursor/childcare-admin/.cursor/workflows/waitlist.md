# Waitlist pack

**When to use:** From their waitlist workbook, list date added, requested room or age band, desired start, and deposit status as they coded it. Order is theirs — do not jump a name for a sibling or a louder email. An opening is their call from the roster, not a promise you make. If two rows share a date and they have no tie-break, list both and ask. Door codes and extra medical notes stay out. Expired or will-call-back rows stay as they labeled them. You do not invent a classroom opening from a remembered ratio law.

**How to run:** Self-contained. Confirm an active Work Item at `work-items/<id>/` (copy `work-items/_TEMPLATE/` if needed). Paths `in/`, `work/`, `out/`, and `evidence/` are inside that folder. Load operations memory, then walk the map: a step is ready when every `needs` artifact exists on disk. Read the named `docs/tools/` file, produce `produce_path`, run `check` from the Work Item folder. On fail, retry at most 3 times, then ask with **operator-qa**. Do not invent a pass. After each step, **journal-keeper**. One ready step per **continue** unless the operator asked for the whole job. Finished pack lands in `out/`. Director gates (start, release, signatures) are not skipped.

**Initial phase:** `role-job`

## Work map

```yaml
id: waitlist
steps:
  - id: list
    needs: []
    produces: wait
    produce_path: work/waitlist.csv
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/csv-has-columns.py work/waitlist.csv child added
    on_fail: retry
    next: [packets]
  - id: packets
    needs: [wait]
    produces: packets
    produce_path: work/waitlist-packets.csv
    tool: docs/tools/enrollment-pdf-folder.md
    check: python docs/tools/checks/file-exists.py work/waitlist-packets.csv
    on_fail: retry
    next: [write]
  - id: write
    needs: [wait, packets]
    produces: wait-pack
    produce_path: out/waitlist.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/waitlist.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects them through **remember**.
