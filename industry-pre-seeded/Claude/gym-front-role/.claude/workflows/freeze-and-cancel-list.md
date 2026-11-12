# Freeze And Cancel List

**When to use:** List open freezes and pending cancels from their freeze log and membership export. Quote freeze length and cancel channel only from their policy and contract files. Do not invent ETF, freeze days, or a cooling-off window. Medical notes stay present-or-missing, not read. Do not mark anyone released. Produce the list plus a pack note in `out/`. They approve holds and they take cancels. Starter until the operator corrects this club’s freeze and cancel files.

**How to run:** Open or reuse `work-items/<id>/` (workflow-selector if unset) → continue one ready YAML step (or the whole named job if requested) → journal-keeper. Paths `work/` and `out/` are inside that Work Item.

**Initial phase:** `intake`

## Work map

```yaml
id: freeze-and-cancel-list
steps:
  - id: log
    needs: []
    produces: freezes
    produce_path: work/freeze-log.csv
    tool: docs/tools/freeze-log.md
    check: python docs/tools/checks/csv-has-columns.py work/freeze-log.csv member_id status
    on_fail: retry
    next: [members]
  - id: members
    needs: [freezes]
    produces: members
    produce_path: work/membership.csv
    tool: docs/tools/membership-export.md
    check: python docs/tools/checks/file-exists.py work/membership.csv
    on_fail: retry
    next: [contracts]
  - id: contracts
    needs: [members]
    produces: contracts
    produce_path: work/contracts-index.csv
    tool: docs/tools/contract-pdf-folder.md
    check: python docs/tools/checks/file-exists.py work/contracts-index.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [freezes, members, contracts]
    produces: freeze-cancel-pack
    produce_path: out/freeze-cancel.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/freeze-cancel.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects this club.
