# Open ROs

**When to use:** List open tickets from their board export or screenshot. One row per RO with their status, promised time, and hold reason. Flag missing authorization, parts holds from their files, and comebacks when history is in the folder. No invented status and no invented ready time. Waiters stay waiters. If the export lacks a column, ask. Do not diagnose. Do not stamp safe or street-legal. Independent and dealer boards both work this way until they teach their status words.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Follow the YAML steps in order: read the named tool doc under `docs/tools/`, write `produce_path` inside this Work Item (`work/` and `out/` mean `work-items/<id>/work/` and `work-items/<id>/out/`), run the listed check against those same paths, then **journal-keeper**. Do not start a step whose `needs` files are missing. On check fail, retry at most three times, then ask. `continue` walks one ready step unless the operator asked for the whole job.

**Initial phase:** `role-job`

## Work map

```yaml
id: open-ros
steps:
  - id: pull
    needs: []
    produces: ro-raw
    produce_path: work/ros.csv
    tool: docs/tools/status-board.md
    check: python docs/tools/checks/csv-has-columns.py work/ros.csv ro status
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [ro-raw]
    produces: ro-pack
    produce_path: out/open-ros.md
    tool: docs/tools/shop-sw.md
    check: python docs/tools/checks/file-exists.py out/open-ros.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects this shop's process (**remember**).
