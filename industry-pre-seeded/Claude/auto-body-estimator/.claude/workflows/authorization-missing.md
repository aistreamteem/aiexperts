# Authorization missing

**When to use:** Compare estimate or supplement dollars to portal screenshots or signed auth they saved. Unapproved lines stay unapproved. Do not invent approved. Teardown auth is a separate yes if their file treats it that way. Write-up is the gap list plus asks, not a hallway go-ahead and not a card. Total-loss on a screenshot stays the insurer's status, not your verdict.

**How to run:** Confirm the Work Item under `work-items/<id>/`. Walk the YAML steps in this file via **continue** (one ready step, or the whole named job if requested). Read the cited `docs/tools/` file, write artifacts under this Work Item’s `work/` and `out/`, run the step `check` against those paths, then **journal-keeper**.

**Initial phase:** first YAML step in this file

## Work map

```yaml
id: authorization-missing
steps:
  - id: est
    needs: []
    produces: est
    produce_path: work/estimate-export.csv
    tool: docs/tools/estimate-export.md
    check: python docs/tools/checks/file-exists.py work/estimate-export.csv
    on_fail: retry
    next: [portal]
  - id: portal
    needs: [est]
    produces: auth
    produce_path: work/auth-status.csv
    tool: docs/tools/insurer-portal-screenshot.md
    check: python docs/tools/checks/file-exists.py work/auth-status.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [est, auth]
    produces: auth-pack
    produce_path: out/authorization-missing.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/authorization-missing.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects this shop's process (**remember**).
