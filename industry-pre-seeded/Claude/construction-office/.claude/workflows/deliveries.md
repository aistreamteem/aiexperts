# Deliveries

**When to use:** List expected and received deliveries for one job. Missing tickets stay missing; a calendar hold is not received. Match each line to a packing slip or photo they filed, and say when the page is absent. Short counts stay on their receiving words. Use their job number on every row. Do not move a truck to a neighboring job. The notes file names ticket numbers as printed. The pack quotes present versus missing backup so later pay or shortage talks have a dated list, not a smoothed story.

**How to run:** Follow `docs/role/work-item-method.md`. Use or create `work-items/<id>/`. Put source files in `in/`. For each YAML step below, in order: (1) do not start if `needs` files are missing — ask the operator; (2) read the `tool` file under `docs/tools/`; (3) write `produce_path` inside this Work Item folder (`work/` and `out/` are relative to the Work Item, not the expert root); (4) run `check` with those same relative paths; (5) on fail, retry at most 3 times then ask via **operator-qa**; (6) update the Work Item journal with **journal-keeper**. After the last step, the pack in `out/` must quote their source files. Do not invent counts, dates, approvals, or answers.

**Initial phase:** `intake`

## Work map

```yaml
id: deliveries
steps:
  - id: list
    needs: []
    produces: deliveries
    produce_path: work/deliveries.csv
    tool: docs/tools/delivery-ticket.md
    check: python docs/tools/checks/csv-has-columns.py work/deliveries.csv date item
    on_fail: retry
    next: [match]
  - id: match
    needs: [deliveries]
    produces: ticket-notes
    produce_path: work/delivery-tickets.md
    tool: docs/tools/delivery-ticket.md
    check: python docs/tools/checks/file-exists.py work/delivery-tickets.md
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [ticket-notes]
    produces: del-pack
    produce_path: out/deliveries.md
    tool: docs/tools/log-sheet.md
    check: python docs/tools/checks/file-exists.py out/deliveries.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they confirm how this shop files.
