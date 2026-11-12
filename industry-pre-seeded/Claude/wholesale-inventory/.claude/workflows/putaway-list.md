# Putaway list

**When to use:** Bins the receiver wrote or preferred locations from their map or master. Do not invent locations. Keep SKU, quantity, UOM, lot or serial if required, and from-dock to-bin if they split. If the map is missing, say so. You do not operate a lift or say a slot is safe. In-transit between dock and bin is not available until they said it landed. One site. Overflow stays a second line if they split bulk and pick face.

**How to run:** Open or switch to a Work Item under `work-items/<id>/`. Follow this YAML one ready step (or the whole named job if requested). Then **journal-keeper**.

**Initial phase:** `role-job`

## Work map

```yaml
id: putaway-list
steps:
  - id: recv
    needs: []
    produces: just-in
    produce_path: work/just-received.csv
    tool: docs/tools/receiving-sheet.md
    check: python docs/tools/checks/csv-has-columns.py work/just-received.csv sku qty
    on_fail: retry
    next: [bins]
  - id: bins
    needs: [just-in]
    produces: putaway
    produce_path: work/putaway.csv
    tool: docs/tools/bin-map.md
    check: python docs/tools/checks/csv-has-columns.py work/putaway.csv sku bin
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [putaway]
    produces: put-pack
    produce_path: out/putaway.md
    tool: docs/tools/bin-map.md
    check: python docs/tools/checks/file-exists.py out/putaway.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects this shop (**remember**).
