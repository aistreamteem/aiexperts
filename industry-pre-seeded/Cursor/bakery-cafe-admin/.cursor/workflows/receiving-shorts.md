# Receiving Shorts

**When to use:** Join the receiving CSV to invoice PDFs they dropped: shorts, damage, qty fights, price only as printed. Do not invent a short or a credit dollar. Do not invent a reject temperature as law. Do not pay. Do not hide a short inside a quieter bake list. The pack is the short list plus asks. They call the vendor; you list the fight.

**How to run:** Self-contained. Active Work Item under `work-items/<id>/`. For each ready step: read the tool doc → write `produce_path` inside that Work Item → run the check with working directory = the Work Item folder → journal-keeper.

**Initial phase:** `recv`

## Work map

```yaml
id: receiving-shorts
steps:
  - id: recv
    needs: []
    produces: recv
    produce_path: work/receiving.csv
    tool: docs/tools/receiving-csv.md
    check: python docs/tools/checks/csv-has-columns.py work/receiving.csv item qty
    on_fail: retry
    next: [inv]
  - id: inv
    needs: [recv]
    produces: inv
    produce_path: work/invoice-index.csv
    tool: docs/tools/invoice-pdf-folder.md
    check: python docs/tools/checks/file-exists.py work/invoice-index.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [recv, inv]
    produces: recv-pack
    produce_path: out/receiving-shorts.md
    tool: docs/tools/receiving-csv.md
    check: python docs/tools/checks/file-exists.py out/receiving-shorts.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator confirms how this shop files (`remember` / `integrate-docs`).
