# Gift acknowledgment drafts

**When to use:** Draft letters from their approved template and the gift file. Fill blanks only. They send and they sign. Do not mark the CSV sent. Do not invent a deductibility sentence, a tax paragraph, or a plate-cost net. Use the matching template for DAF, stock, or event if they named one. Quid pro quo estimates come from their event file. A draft in out/ is not an issued acknowledgment. If no template is present, ask; do not write Publication 1771 wording from memory as if it were letterhead.

**How to run:** Open or continue the Work Item under `work-items/<id>/`. Walk one ready YAML step (or the whole named job if requested): produce the file, run the check, then journal-keeper.

**Initial phase:** `role-job`

## Work map

```yaml
id: gift-ack-draft
steps:
  - id: gifts
    needs: []
    produces: gifts
    produce_path: work/gifts.csv
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py work/gifts.csv
    on_fail: retry
    next: [tmpl]
  - id: tmpl
    needs: [gifts]
    produces: template
    produce_path: work/ack-template.md
    tool: docs/tools/ack-template.md
    check: python docs/tools/checks/file-exists.py work/ack-template.md
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [gifts, template]
    produces: ack-out
    produce_path: out/ack-drafts.md
    tool: docs/tools/ack-template.md
    check: python docs/tools/checks/file-exists.py out/ack-drafts.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct how this shop works (**remember**).
