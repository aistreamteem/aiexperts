# Tracking Exceptions

**When to use:** From the carrier export, list exception codes, failed delivery, and trackers that never appeared after a label PDF. Do not invent a tracking number or a delivered time. Voided labels stay off the live list. Do not promise a new delivery day. POD presence is yes/no from their file. They call the carrier. You do not pay a claim. Multi-piece orders missing one tracker stay listed piece by piece. You do not invent POD. They call the carrier. Claim dollars stay off this pack unless they asked for a separate claim-file routing.

**How to run:** Open or switch to a Work Item under `work-items/<id>/`. Put source files in that item’s `in/`. Follow the YAML steps below — one ready step per **continue**, or the whole named job if requested. Read the named `docs/tools/` doc. Produce files under this Work Item. Run each step’s check. Then **journal-keeper**.

**Initial phase:** `role-job`

## Work map

```yaml
id: tracking-exceptions
steps:
  - id: labels
    needs: []
    produces: labels
    produce_path: work/labels-index.csv
    tool: docs/tools/label-pdf-folder.md
    check: python docs/tools/checks/file-exists.py work/labels-index.csv
    on_fail: retry
    next: [carrier]
  - id: carrier
    needs: [labels]
    produces: carrier
    produce_path: work/carrier.csv
    tool: docs/tools/carrier-export.md
    check: python docs/tools/checks/file-exists.py work/carrier.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [labels, carrier]
    produces: track-pack
    produce_path: out/tracking-exceptions.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/tracking-exceptions.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they **remember** a shop correction.
