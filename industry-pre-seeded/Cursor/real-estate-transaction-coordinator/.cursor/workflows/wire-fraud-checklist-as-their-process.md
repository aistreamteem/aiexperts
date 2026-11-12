# Wire Fraud Checklist as Their Process

**When to use:** Assemble their written verify-before-wire process and a reminder-log row if they asked you to log it. Never send, retype, or store wire instructions or account numbers. New wiring in an email is an unverified flag, not the destination. They verify by a known number. Title confirms. The pack is a process checklist plus present-or-missing reminder evidence, not a payment. FBI and FTC pages are orientation only. You never move funds.

**How to run:** open or select a Work Item under `work-items/<id>/` → follow this file one ready step (or the whole named job if requested) → journal-keeper

**Initial phase:** `role-job`

## Work map

```yaml
id: wire-fraud-checklist-as-their-process
steps:
  - id: process
    needs: []
    produces: wire-process
    produce_path: work/wire-process.csv
    tool: docs/tools/checklist-sheet.md
    check: python docs/tools/checks/csv-has-columns.py work/wire-process.csv step status
    on_fail: retry
    next: [log]
  - id: log
    needs: [wire-process]
    produces: wire-log
    produce_path: work/wire-checklist.csv
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py work/wire-checklist.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [wire-process, wire-log]
    produces: wire-pack
    produce_path: out/wire-fraud-checklist.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/wire-fraud-checklist.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this shop.
