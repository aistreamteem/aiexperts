# Custom Cake Board

**When to use:** List open cake and wedding tickets from the cake-order folder against the production calendar: due, flavor-from-menu, size, filling and buttercream names, deposit flag, photo present yes/no. Do not invent a formula, servings, or a due the calendar cannot meet. Do not store PAN. Tasting notes are not tickets. The pack is the board plus missing fields. They bake and decorate; you board.

**How to run:** Self-contained. Active Work Item under `work-items/<id>/`. For each ready step: read the tool doc → write `produce_path` inside that Work Item → run the check with working directory = the Work Item folder → journal-keeper.

**Initial phase:** `orders`

## Work map

```yaml
id: custom-cake-board
steps:
  - id: orders
    needs: []
    produces: orders
    produce_path: work/cake-orders.csv
    tool: docs/tools/cake-order-folder.md
    check: python docs/tools/checks/file-exists.py work/cake-orders.csv
    on_fail: retry
    next: [cal]
  - id: cal
    needs: [orders]
    produces: cal
    produce_path: work/production-calendar.csv
    tool: docs/tools/calendar.md
    check: python docs/tools/checks/file-exists.py work/production-calendar.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [orders, cal]
    produces: cake-pack
    produce_path: out/custom-cake-board.md
    tool: docs/tools/cake-order-folder.md
    check: python docs/tools/checks/file-exists.py out/custom-cake-board.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator confirms how this shop files (`remember` / `integrate-docs`).
