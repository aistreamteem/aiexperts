# Licensing packet completeness

**When to use:** Against their visit checklist, list named binder pages as present or missing: posted license, drill log, menus, staff-file dates, and enrollment samples they asked you to sample. Do not invent a statute or stamp the center compliant. Staff credentials are dates on file, not a license you grant. Children’s medical pages stay present-or-missing without extra clinical copy into docs/. If their checklist and a state packet they saved disagree, quote both and ask. This pack is a completeness list for the director, not an inspector signature.

**How to run:** Self-contained. Confirm an active Work Item at `work-items/<id>/` (copy `work-items/_TEMPLATE/` if needed). Paths `in/`, `work/`, `out/`, and `evidence/` are inside that folder. Load operations memory, then walk the map: a step is ready when every `needs` artifact exists on disk. Read the named `docs/tools/` file, produce `produce_path`, run `check` from the Work Item folder. On fail, retry at most 3 times, then ask with **operator-qa**. Do not invent a pass. After each step, **journal-keeper**. One ready step per **continue** unless the operator asked for the whole job. Finished pack lands in `out/`. Director gates (start, release, signatures) are not skipped.

**Initial phase:** `role-job`

## Work map

```yaml
id: licensing-packet-completeness
steps:
  - id: binder
    needs: []
    produces: binder
    produce_path: work/licensing-index.csv
    tool: docs/tools/licensing-forms-folder.md
    check: python docs/tools/checks/file-exists.py work/licensing-index.csv
    on_fail: retry
    next: [staff]
  - id: staff
    needs: [binder]
    produces: staff
    produce_path: work/staff-index.csv
    tool: docs/tools/staff-file-index.md
    check: python docs/tools/checks/csv-has-columns.py work/staff-index.csv staff date
    on_fail: retry
    next: [write]
  - id: write
    needs: [binder, staff]
    produces: lic-pack
    produce_path: out/licensing-completeness.md
    tool: docs/tools/licensing-forms-folder.md
    check: python docs/tools/checks/file-exists.py out/licensing-completeness.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects them through **remember**.
