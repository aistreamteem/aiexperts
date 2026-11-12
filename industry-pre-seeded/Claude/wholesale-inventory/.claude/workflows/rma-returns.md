# Returns / RMA pack

**When to use:** Condition and sellable flag from their RMA sheet. Do not credit. Do not add to good stock unless they said so. Keep RMA number, SKU, quantity, UOM, and lot or serial if required. Missing RMA is an exception, not a number you invent. Salvage and quarantine stay out of available. Return-to-vendor needs their vendor authorization if they stored it. You do not dump damaged goods. Quote their status words in the pack.

**How to run:** Open or switch to a Work Item under `work-items/<id>/`. Follow this YAML one ready step (or the whole named job if requested). Then **journal-keeper**.

**Initial phase:** `role-job`

## Work map

```yaml
id: rma-returns
steps:
  - id: list
    needs: []
    produces: rmas
    produce_path: work/rmas.csv
    tool: docs/tools/rma-form.md
    check: python docs/tools/checks/csv-has-columns.py work/rmas.csv rma sku qty
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [rmas]
    produces: rma-pack
    produce_path: out/rmas.md
    tool: docs/tools/rma-form.md
    check: python docs/tools/checks/file-exists.py out/rmas.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects this shop (**remember**).
