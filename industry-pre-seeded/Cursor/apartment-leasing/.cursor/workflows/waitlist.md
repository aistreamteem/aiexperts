# Waitlist

**When to use:** Read their waitlist CSV in the existing order and write the pack. Do not jump a row. Do not mix a market list with an affordable program list. A seat is not a hold and not an approval. Expire a row only if their policy file already says to. They decide whom to call when a unit comes up. Ask if the date-joined column is missing.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put their waitlist CSV in `in/`. Read this file and `docs/tools/spreadsheet.md`. Walk one ready YAML step (or the whole job if requested): produce the file under this Work Item’s `work/` or `out/`, run the check, then journal-keeper. Do not skip a step with a chat summary.

**Initial phase:** `role-job`

## Work map

```yaml
id: waitlist
steps:
  - id: list
    needs: []
    produces: list
    produce_path: work/waitlist.csv
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/csv-has-columns.py work/waitlist.csv name date
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [list]
    produces: waitlist-pack
    produce_path: out/waitlist.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/waitlist.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects this shop (remember / integrate-docs).
