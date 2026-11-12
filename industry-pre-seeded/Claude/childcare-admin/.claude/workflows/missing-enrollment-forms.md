# Missing Enrollment Forms

**When to use:** From the enrollment PDF folder, list each named packet page as present, dated, signed, or missing for the children they asked. Do not fill blanks. Do not copy full SSN or extra medical notes into docs/. Guardian signatures are present or missing, not a custody decision. A packet that is almost done is still incomplete. Sibling children are separate rows. Start without a complete packet is their written exception, not your mark.

**How to run:** Self-contained. Confirm an active Work Item at `work-items/<id>/` (copy `work-items/_TEMPLATE/` if needed). Paths `in/`, `work/`, `out/`, and `evidence/` are inside that folder. Load operations memory, then walk the map: a step is ready when every `needs` artifact exists on disk. Read the named `docs/tools/` file, produce `produce_path`, run `check` from the Work Item folder. On fail, retry at most 3 times, then ask with **operator-qa**. Do not invent a pass. After each step, **journal-keeper**. One ready step per **continue** unless the operator asked for the whole job. Finished pack lands in `out/`. Director gates (start, release, signatures) are not skipped.

**Initial phase:** `role-job`

## Work map

```yaml
id: missing-enrollment-forms
steps:
  - id: folder
    needs: []
    produces: packets
    produce_path: work/packet-index.csv
    tool: docs/tools/enrollment-pdf-folder.md
    check: python docs/tools/checks/file-exists.py work/packet-index.csv
    on_fail: retry
    next: [grid]
  - id: grid
    needs: [packets]
    produces: grid
    produce_path: work/missing-forms.csv
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/csv-has-columns.py work/missing-forms.csv child form complete
    on_fail: retry
    next: [write]
  - id: write
    needs: [packets, grid]
    produces: forms-pack
    produce_path: out/missing-enrollment-forms.md
    tool: docs/tools/enrollment-pdf-folder.md
    check: python docs/tools/checks/file-exists.py out/missing-enrollment-forms.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects them through **remember**.
