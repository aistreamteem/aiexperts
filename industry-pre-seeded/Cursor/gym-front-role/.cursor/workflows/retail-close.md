# Retail close

**When to use:** Close retail from their count-and-price sheet plus the day-close tender export. Keep backbar off the sold pile if they split bins. Do not invent a price, a bottle count, or a cash-drawer total. Counted cash is a number they type after they count. No diet advice on shake SKUs. Produce the close pack plus a pack note. They sell and they count the drawer. Starter until they teach this club’s official close report.

**How to run:** Open or continue the Work Item under `work-items/<id>/`. Follow this file's YAML via **continue**. Read the cited `docs/tools/` doc, write artifacts under the Work Item, run the step `check`, store logs in `evidence/`, then **journal-keeper**.

**Initial phase:** `role-job`

## Work map

```yaml
id: retail-close
steps:
  - id: retail
    needs: []
    produces: retail
    produce_path: work/retail.csv
    tool: docs/tools/retail-sheet.md
    check: python docs/tools/checks/csv-has-columns.py work/retail.csv sku price
    on_fail: retry
    next: [tender]
  - id: tender
    needs: [retail]
    produces: tender
    produce_path: work/day-close.csv
    tool: docs/tools/day-close-tender.md
    check: python docs/tools/checks/file-exists.py work/day-close.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [retail, tender]
    produces: retail-pack
    produce_path: out/retail-close.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/retail-close.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects this shop.
