# Traffic Log

**When to use:** Pull guest cards, tally source labels as written, and write a traffic pack. Do not invent a source to fill a quiet day. Same-day duplicates stay two rows unless their file says to merge. Traffic is not applications or move-ins. Do not copy phone numbers into extra docs if the source list does not need them. They use the pack; you do not change ads.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put guest-card exports in `in/`. Read this file and `docs/tools/guest-card-sheet.md`. Walk one ready YAML step (or the whole job if requested): produce the file under this Work Item’s `work/` or `out/`, run the check, then journal-keeper. Do not skip a step with a chat summary.

**Initial phase:** `role-job`

## Work map

```yaml
id: traffic-log
steps:
  - id: cards
    needs: []
    produces: cards
    produce_path: work/guest-cards.csv
    tool: docs/tools/guest-card-sheet.md
    check: python docs/tools/checks/csv-has-columns.py work/guest-cards.csv name date source
    on_fail: retry
    next: [sources]
  - id: sources
    needs: [cards]
    produces: sources
    produce_path: work/traffic-sources.csv
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/csv-has-columns.py work/traffic-sources.csv source count
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [cards, sources]
    produces: traffic-pack
    produce_path: out/traffic-log.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/traffic-log.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects this shop (remember / integrate-docs).
