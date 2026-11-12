# Backorder and late-line list

**When to use:** Build a list of open lines past need-by, plus vendor backorder notes from the latest PDF or acknowledgment. Promise dates only from that file — not from hope or a remembered lead time. They contact the vendor unless they asked you only to list. Do not overwrite need-by with a late promise. Do not zero remaining qty. Infeasible original need-by stays flagged if the PDF never supported it. Cancel or close-short is their decision.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put source files in `in/`. Read this file and the named `docs/tools/` doc. Walk one ready YAML step (or the whole named job if requested): produce the file under this Work Item’s `work/` or `out/`, run the check, then journal-keeper. Do not skip a step with a chat summary.

**Initial phase:** `role-job`

## Work map

```yaml
id: backorder-list
steps:
  - id: pos
    needs: []
    produces: pos
    produce_path: work/pos.csv
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/csv-has-columns.py work/pos.csv po sku qty
    on_fail: retry
    next: [pdf]
  - id: pdf
    needs: [pos]
    produces: notes
    produce_path: work/vendor-notes.csv
    tool: docs/tools/vendor-pdf.md
    check: python docs/tools/checks/file-exists.py work/vendor-notes.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [pos, notes]
    produces: late-pack
    produce_path: out/backorders.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/backorders.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this shop (**remember**).
