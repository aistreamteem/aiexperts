# Late List

**When to use:** From payment-status and their late export, list units coded past due with paid-through or days late as they printed. Do not invent a late fee. Do not say a lien attached or that they may auction. Overlock is a status if they coded it, never a code in docs. Autopay failed is a flag, not a card you rerun. Military flags stay visible if present. They contact occupants. You pack the list and fee-file asks.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put payment-status and late exports in `in/`. Read this file and `docs/tools/payment-status-export.md` / `docs/tools/late-list.md`. Walk one ready YAML step (or the whole job if requested): produce the file under this Work Item’s `work/` or `out/`, run the check, then journal-keeper. Do not skip a step with a chat summary.

**Initial phase:** `role-job`

## Work map

```yaml
id: late-list
steps:
  - id: status
    needs: []
    produces: pay
    produce_path: work/payment-status.csv
    tool: docs/tools/payment-status-export.md
    check: python docs/tools/checks/csv-has-columns.py work/payment-status.csv unit status
    on_fail: retry
    next: [late]
  - id: late
    needs: [pay]
    produces: late
    produce_path: work/late-list.csv
    tool: docs/tools/late-list.md
    check: python docs/tools/checks/csv-has-columns.py work/late-list.csv unit status
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [pay, late]
    produces: late-pack
    produce_path: out/late-list.md
    tool: docs/tools/late-list.md
    check: python docs/tools/checks/file-exists.py out/late-list.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects this shop via **remember**.
