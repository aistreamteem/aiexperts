# Fill Vs Open

**When to use:** Join job orders to assignments. Count filled versus open with their status words and their fill-rate formula only. Do not invent a formula. Do not drop cancelled orders unless their math says to. Do not mark filled without their filled assignment. Label the period. Write the counts, the ratio if they defined one, and a pack. Not a CRM dashboard. They define filled. You show the math from their files.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put job orders and assignments in `in/`. Read this file and the named `docs/tools/` doc. Walk one ready YAML step (or the whole job if requested): produce the file under this Work Item’s `work/` or `out/`, run the check, then journal-keeper. Do not skip a step with a chat summary.

**Initial phase:** `role-job`

## Work map

```yaml
id: fill-vs-open
steps:
  - id: orders
    needs: []
    produces: orders
    produce_path: work/job-orders.csv
    tool: docs/tools/job-order-folder.md
    check: python docs/tools/checks/csv-has-columns.py work/job-orders.csv order status
    on_fail: retry
    next: [assign]
  - id: assign
    needs: [orders]
    produces: assign
    produce_path: work/assignments.csv
    tool: docs/tools/assignment-sheet.md
    check: python docs/tools/checks/file-exists.py work/assignments.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [orders, assign]
    produces: fill-pack
    produce_path: out/fill-vs-open.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/fill-vs-open.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this shop.
