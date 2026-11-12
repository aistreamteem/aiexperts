# Delivery Tickets

**When to use:** List today’s delivery and pickup tickets with zone lookup from their zone sheet. Do not invent miles, a zone letter, or an ETA. Missing site address is an ask. After-hours flags copy from the ticket or hours file. Gate codes stay out of the pack. Maintenance-due units still on the truck list are conflicts. You do not pay the hauler. Produce the run list and exception pack. They dispatch.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Follow this file one ready step (or the whole named job if requested). Read the named tool under `docs/tools/`. Write artifacts under this Work Item (`work/` and `out/` mean `work-items/<id>/work/` and `work-items/<id>/out/`). Run the step check against those paths. After each step, run **journal-keeper**. If a required file or shop rule is missing, ask (**operator-qa** when the answer would change the pack). Do not invent rates, meters, serials, zones, deposits, or fees.

**Initial phase:** `role-job`

## Work map

```yaml
id: delivery-tickets
steps:
  - id: tix
    needs: []
    produces: tickets
    produce_path: work/delivery-tickets.csv
    tool: docs/tools/delivery-ticket-folder.md
    check: python docs/tools/checks/file-exists.py work/delivery-tickets.csv
    on_fail: retry
    next: [zone]
  - id: zone
    needs: [tickets]
    produces: zones
    produce_path: work/zones.csv
    tool: docs/tools/zone-sheet.md
    check: python docs/tools/checks/file-exists.py work/zones.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [tickets, zones]
    produces: del-pack
    produce_path: out/delivery-tickets.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/delivery-tickets.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator confirms this yard's process (save with **remember**).
