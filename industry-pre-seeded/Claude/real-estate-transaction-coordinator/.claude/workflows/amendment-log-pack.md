# Amendment Log Pack

**When to use:** Build one dated log of every executed amendment against the live contract file: what changed, old versus new, signatures, and filename. Drafts and emails stay labeled not executed unless their process says otherwise. Do not rewrite the original PDF. Do not invent a credit or a new closing date. If two versions both look signed, quote both and ask which is live. They circulate. You keep the log readable for the dates calendar and the closing checklist.

**How to run:** open or select a Work Item under `work-items/<id>/` → follow this file one ready step (or the whole named job if requested) → journal-keeper

**Initial phase:** `role-job`

## Work map

```yaml
id: amendment-log-pack
steps:
  - id: log
    needs: []
    produces: amendments
    produce_path: work/amendment-log.csv
    tool: docs/tools/amendment-log.md
    check: python docs/tools/checks/csv-has-columns.py work/amendment-log.csv date change
    on_fail: retry
    next: [contract]
  - id: contract
    needs: [amendments]
    produces: contract-index
    produce_path: work/contract-index.csv
    tool: docs/tools/contract-pdf.md
    check: python docs/tools/checks/file-exists.py work/contract-index.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [amendments, contract-index]
    produces: amendment-pack
    produce_path: out/amendment-log.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/amendment-log.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this shop.
