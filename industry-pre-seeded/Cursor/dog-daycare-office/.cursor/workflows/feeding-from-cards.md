# Feeding From Cards

**When to use:** Transcribe feeding as the client wrote it onto the feeding sheet for the stay date. Do not substitute a bag or invent cups. Unreadable lines are questions. Allergy words stay theirs, not a diagnosis. Confirm the occupancy list so you do not feed a dog who is not here. House food is only a named backup on their sheet. Starter / guess until they teach who initials the clipboard.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put source files in `in/`. Walk one ready YAML step (or the whole named job if requested): read the named tool doc, produce the file, run the check, then **journal-keeper**.

**Initial phase:** `role-job`

## Work map

```yaml
id: feeding-from-cards
steps:
  - id: cards
    needs: []
    produces: cards
    produce_path: work/boarding.csv
    tool: docs/tools/boarding-csv.md
    check: python docs/tools/checks/csv-has-columns.py work/boarding.csv patient stay
    on_fail: retry
    next: [sheet]
  - id: sheet
    needs: [cards]
    produces: feed
    produce_path: work/feeding.csv
    tool: docs/tools/feeding-sheet.md
    check: python docs/tools/checks/csv-has-columns.py work/feeding.csv patient food
    on_fail: retry
    next: [write]
  - id: write
    needs: [cards, feed]
    produces: feed-pack
    produce_path: out/feeding-from-cards.md
    tool: docs/tools/feeding-sheet.md
    check: python docs/tools/checks/file-exists.py out/feeding-from-cards.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this shop.
