# Open Job Orders

**When to use:** Index the job-order folder and client list. List orders they still code as open or partial-fill: client, shift, remaining headcount as they count filled, start window, and missing description or rate pointers. Do not invent an order. Do not close an order to improve fill. Do not build a CRM pipeline. Write the open list and a pack. They fill. Cancelled and on-hold stay as they coded them.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put job-order folder and client list in `in/`. Read this file and the named `docs/tools/` doc. Walk one ready YAML step (or the whole job if requested): produce the file under this Work Item’s `work/` or `out/`, run the check, then journal-keeper. Do not skip a step with a chat summary.

**Initial phase:** `role-job`

## Work map

```yaml
id: open-job-orders
steps:
  - id: orders
    needs: []
    produces: orders
    produce_path: work/job-orders.csv
    tool: docs/tools/job-order-folder.md
    check: python docs/tools/checks/csv-has-columns.py work/job-orders.csv order status
    on_fail: retry
    next: [clients]
  - id: clients
    needs: [orders]
    produces: clients
    produce_path: work/clients.csv
    tool: docs/tools/client-list.md
    check: python docs/tools/checks/file-exists.py work/clients.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [orders, clients]
    produces: open-pack
    produce_path: out/open-job-orders.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/open-job-orders.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this shop.
