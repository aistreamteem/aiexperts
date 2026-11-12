# Pickup Invoice

**When to use:** Compare last authorization and technician notes to the invoice PDF. Flag extras, missing declined lines, returned parts still billed, and total mismatches as questions. You do not change a total. You do not invent a correction. Warranty language quotes their sheet only. Independent and dealer pickup counters both need this check. Cause and correction on billed repair must be in the tech file or listed missing. No card numbers. Ready is their QC flag, not a safe-to-drive sentence you add.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Follow the YAML steps in order: read the named tool doc under `docs/tools/`, write `produce_path` inside this Work Item (`work/` and `out/` mean `work-items/<id>/work/` and `work-items/<id>/out/`), run the listed check against those same paths, then **journal-keeper**. Do not start a step whose `needs` files are missing. On check fail, retry at most three times, then ask. `continue` walks one ready step unless the operator asked for the whole job.

**Initial phase:** `role-job`

## Work map

```yaml
id: pickup-invoice
steps:
  - id: inv
    needs: []
    produces: inv-raw
    produce_path: work/invoice-lines.csv
    tool: docs/tools/ro-pdf.md
    check: python docs/tools/checks/csv-has-columns.py work/invoice-lines.csv line amount
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [inv-raw]
    produces: invoice-pack
    produce_path: out/pickup-check.md
    tool: docs/tools/warranty-file.md
    check: python docs/tools/checks/file-exists.py out/pickup-check.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects this shop's process (**remember**).
