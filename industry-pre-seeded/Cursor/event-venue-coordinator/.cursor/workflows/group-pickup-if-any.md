# Group pickup (if any)

**When to use:** If they have a sleeping-room block file, list contracted rooms, pickup, remaining, printed rate, and room cutoff. If the file is empty, say no block — do not invent one. Do not invent pickup or a group rate. Do not wash rooms. Banquet minimum stays on banquet files. They manage the hotel system. You deliver the pickup pack when a block exists.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put the group-block file in `in/` if one exists. Read this file and `docs/tools/group-block-if-any.md` / `docs/tools/spreadsheet.md`. Walk one ready YAML step (or the whole job if requested): produce the file under this Work Item’s `work/` or `out/`, run the check, then journal-keeper. Do not skip a step with a chat summary.

**Initial phase:** `role-job`

## Work map

```yaml
id: group-pickup-if-any
steps:
  - id: block
    needs: []
    produces: block
    produce_path: work/group-block.csv
    tool: docs/tools/group-block-if-any.md
    check: python docs/tools/checks/file-exists.py work/group-block.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [block]
    produces: pickup-pack
    produce_path: out/group-pickup.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/group-pickup.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects this shop (remember / integrate-docs).
