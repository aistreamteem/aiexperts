# Day Close

**When to use:** From their close report, list production, collection, and tender totals as exported. Variances are questions. You do not take the deposit. Do not treat production as cash in the drawer. Do not reallocate provider production. Do not create a write-off to force a match. Card numbers stay out. Cash, check, card, and electronic totals stay as their tape or system shows. One date and one location. Ask if a batch posts on the next banking day before you call cash missing.

**How to run:** Open or reuse `work-items/<id>/`. Put the source export in `in/`. Follow this map in order: read the named `docs/tools/` file, write `produce_path` inside this Work Item, run the step `check`, retry at most 3 times on fail then ask. Pass produced files to the next step. One ready step per continue unless the operator asked for the whole job. Then journal-keeper.

**Initial phase:** `role-job`

## Work map

```yaml
id: day-close
steps:
  - id: pull
    needs: []
    produces: close-raw
    produce_path: work/day-close.csv
    tool: docs/tools/pms-export.md
    check: python docs/tools/checks/file-exists.py work/day-close.csv
    on_fail: retry
    next: [write]
  - id: write
    needs: [close-raw]
    produces: close-writeup
    produce_path: out/day-close.md
    tool: docs/tools/pms-export.md
    check: python docs/tools/checks/file-exists.py out/day-close.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator confirms how this office works.
