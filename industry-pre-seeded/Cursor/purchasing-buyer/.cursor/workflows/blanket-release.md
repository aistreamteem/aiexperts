# Blanket Release

**When to use:** Draft a release against the blanket log: keep the blanket number on every line, remaining not-to-exceed or remaining qty if they track it, release quantity, and the blanket price file. Do not invent remaining value and do not use a contradicting one-off price without asking. The release stays a draft. They approve and they send. Exceeding remaining NTE is a question, not a quiet extra. Need-by still comes from their requisition or plan, not from a guessed date.

**How to run:** Select this job with workflow-selector (or continue). Use `work-items/<id>/`. Put source files in `in/`. Walk one ready step: read the named tool doc, write the produced file under this Work Item, run the check, then journal-keeper. Do not skip a step with a chat summary. Whole named job only if they asked.

**Initial phase:** `role-job`

## Work map

```yaml
id: blanket-release
steps:
  - id: blanket
    needs: []
    produces: blanket
    produce_path: work/blanket-log.csv
    tool: docs/tools/blanket-log.md
    check: python docs/tools/checks/csv-has-columns.py work/blanket-log.csv blanket_po
    on_fail: retry
    next: [rel]
  - id: rel
    needs: [blanket]
    produces: release
    produce_path: work/release.csv
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py work/release.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [blanket, release]
    produces: rel-pack
    produce_path: out/blanket-release.md
    tool: docs/tools/blanket-log.md
    check: python docs/tools/checks/file-exists.py out/blanket-release.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they confirm how *this* shop files and checks the pack.
