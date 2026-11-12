# Delivery Today

**When to use:** List jobs that should leave today from the delivery log and matching tickets: method, ship-to, carton or pallet count, and POD if they collect one. Do not invent a delivery day. Short drops stay short. Split ships need a row per drop. You do not pay a carrier and you do not store PAN. The pack is today's route or will-call list plus qty fights.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put source files in `in/`. Walk one ready YAML step (or the whole named job if requested): produce the file, run the check, then **journal-keeper**.

**Initial phase:** isolate / intake

## Work map

```yaml
id: delivery-today
steps:
  - id: del
    needs: []
    produces: delivery
    produce_path: work/delivery-log.csv
    tool: docs/tools/delivery-log.md
    check: python docs/tools/checks/csv-has-columns.py work/delivery-log.csv job qty
    on_fail: retry
    next: [tickets]
  - id: tickets
    needs: [delivery]
    produces: tickets
    produce_path: work/job-tickets.csv
    tool: docs/tools/job-ticket-sheet.md
    check: python docs/tools/checks/file-exists.py work/job-tickets.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [delivery, tickets]
    produces: delivery-pack
    produce_path: out/delivery-today.md
    tool: docs/tools/delivery-log.md
    check: python docs/tools/checks/file-exists.py out/delivery-today.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they **remember** a correction for this shop.
