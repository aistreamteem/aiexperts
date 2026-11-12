# Bindery Queue

**When to use:** Build a finishing queue from the bindery list and open tickets: cut, fold, stitch, laminate, drill, insert, kit in their order. Press-complete is not ship-complete. Do not skip a step to make due-today possible. Do not invent bindery hours. Outside bindery stays a vendor note, not a payment. The pack is the queue plus tickets waiting on a prior step. Due dates still read against their calendar.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put source files in `in/`. Walk one ready YAML step (or the whole named job if requested): produce the file, run the check, then **journal-keeper**.

**Initial phase:** isolate / intake

## Work map

```yaml
id: bindery-queue
steps:
  - id: bind
    needs: []
    produces: bindery
    produce_path: work/bindery-list.csv
    tool: docs/tools/bindery-list.md
    check: python docs/tools/checks/file-exists.py work/bindery-list.csv
    on_fail: retry
    next: [tickets]
  - id: tickets
    needs: [bindery]
    produces: tickets
    produce_path: work/job-tickets.csv
    tool: docs/tools/job-ticket-sheet.md
    check: python docs/tools/checks/file-exists.py work/job-tickets.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [bindery, tickets]
    produces: bindery-pack
    produce_path: out/bindery-queue.md
    tool: docs/tools/bindery-list.md
    check: python docs/tools/checks/file-exists.py out/bindery-queue.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they **remember** a correction for this shop.
