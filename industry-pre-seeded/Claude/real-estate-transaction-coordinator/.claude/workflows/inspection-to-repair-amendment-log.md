# Inspection to Repair Amendment Log

**When to use:** Index inspection PDFs by type and date, then list any executed repair amendment that followed. Inspector comments are not contract language. Credits and repair lists come only from signed pages. Unsigned drafts stay drafts. Do not invent a credit to match a bid. Do not steer the next inspector. Show old versus new if a later amendment changed the first. They negotiate. You keep the log. Walkthrough punch items stay off this pack unless they asked to attach them as leftover work.

**How to run:** open or select a Work Item under `work-items/<id>/` → follow this file one ready step (or the whole named job if requested) → journal-keeper

**Initial phase:** `role-job`

## Work map

```yaml
id: inspection-to-repair-amendment-log
steps:
  - id: inspections
    needs: []
    produces: inspections
    produce_path: work/inspections.csv
    tool: docs/tools/inspection-pdf-folder.md
    check: python docs/tools/checks/csv-has-columns.py work/inspections.csv report_type date
    on_fail: retry
    next: [amendments]
  - id: amendments
    needs: [inspections]
    produces: repairs
    produce_path: work/repair-amendments.csv
    tool: docs/tools/amendment-log.md
    check: python docs/tools/checks/file-exists.py work/repair-amendments.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [inspections, repairs]
    produces: repair-pack
    produce_path: out/inspection-repair.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/inspection-repair.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this shop.
