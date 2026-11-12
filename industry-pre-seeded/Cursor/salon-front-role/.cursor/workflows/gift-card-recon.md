# Gift Card Recon

**When to use:** From their gift-card export, list sales, redemptions, and remaining balances using last-four or internal IDs only. No full card numbers. Liability is not the same as today’s service revenue. Do not invent a remaining balance. Packages stay on their own lines if the export splits them. You do not issue or refund. They handle guest questions. Starter until they teach this shop’s gift-card report.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put source files in that item's `in/`. Walk one ready YAML step (or the whole named job if requested): produce the file, run the check, then **journal-keeper**. Paths `in/`, `work/`, `out/`, and `evidence/` are inside that Work Item.

**Initial phase:** `role-job`

## Work map

```yaml
id: gift-card-recon
steps:
  - id: pull
    needs: []
    produces: gc
    produce_path: work/gift-cards.csv
    tool: docs/tools/gift-card-export.md
    check: python docs/tools/checks/file-exists.py work/gift-cards.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [gc]
    produces: gc-pack
    produce_path: out/gift-cards.md
    tool: docs/tools/gift-card-export.md
    check: python docs/tools/checks/file-exists.py out/gift-cards.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects this shop (**remember**).
