# Lease Packet

**When to use:** Index the lease-packet folder, tick addenda against their checklist, and write the pack. Completeness only — no legal review and no invented riders. Lead pamphlet present or missing if their checklist calls for it on pre-1978 homes. Concession addenda must match the specials file if that file is in the folder; do not invent a special. They send the packet.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put the lease-packet folder contents in `in/`. Read this file and `docs/tools/lease-packet-folder.md`. Walk one ready YAML step (or the whole job if requested): produce the file under this Work Item’s `work/` or `out/`, run the check, then journal-keeper. Do not skip a step with a chat summary.

**Initial phase:** `role-job`

## Work map

```yaml
id: lease-packet
steps:
  - id: folder
    needs: []
    produces: folder
    produce_path: work/packet-index.csv
    tool: docs/tools/lease-packet-folder.md
    check: python docs/tools/checks/file-exists.py work/packet-index.csv
    on_fail: retry
    next: [checklist]
  - id: checklist
    needs: [folder]
    produces: checklist
    produce_path: work/addendum-checklist.csv
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/csv-has-columns.py work/addendum-checklist.csv addendum required
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [folder, checklist]
    produces: packet-pack
    produce_path: out/lease-packet.md
    tool: docs/tools/lease-packet-folder.md
    check: python docs/tools/checks/file-exists.py out/lease-packet.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects this shop (remember / integrate-docs).
