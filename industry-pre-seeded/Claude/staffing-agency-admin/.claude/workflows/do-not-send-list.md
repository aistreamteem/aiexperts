# Do Not Send List

**When to use:** From the employee list and client list, print people flagged DNS or DNR with the scope they coded — one site versus all. Do not invent a flag. Do not fire anyone. Do not write a legal reason. Background dates stay dates, not a verdict you stamp. Write the blocked list and a pack so the assignment board can filter. They own the flags. You list who is not to be sent.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put employee list and client list in `in/`. Read this file and the named `docs/tools/` doc. Walk one ready YAML step (or the whole job if requested): produce the file under this Work Item’s `work/` or `out/`, run the check, then journal-keeper. Do not skip a step with a chat summary.

**Initial phase:** `role-job`

## Work map

```yaml
id: do-not-send-list
steps:
  - id: people
    needs: []
    produces: people
    produce_path: work/employee-list.csv
    tool: docs/tools/employee-list.md
    check: python docs/tools/checks/csv-has-columns.py work/employee-list.csv name
    on_fail: retry
    next: [clients]
  - id: clients
    needs: [people]
    produces: clients
    produce_path: work/clients.csv
    tool: docs/tools/client-list.md
    check: python docs/tools/checks/file-exists.py work/clients.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [people, clients]
    produces: dns-pack
    produce_path: out/do-not-send.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/do-not-send.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this shop.
