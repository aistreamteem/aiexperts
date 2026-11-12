# Days Book

**When to use:** Build tomorrow’s or today’s book from their booking export. Flag stylist clashes, blank providers, and slots outside the hours file. Do not move guests. Pending online rows stay pending. Walk-ins need a slot type they already use. Guest labels stay as exported. Produce the book pack they can read; they contact guests and they decide any move. Hours file beats a stray widget slot. Starter until they teach this floor’s labels.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put source files in that item’s `in/`. Walk one ready YAML step (or the whole named job if requested): produce the file, run the check, then **journal-keeper**. Paths `in/`, `work/`, `out/`, and `evidence/` are inside that Work Item.

**Initial phase:** `role-job`

## Work map

```yaml
id: days-book
steps:
  - id: pull
    needs: []
    produces: book
    produce_path: work/book.csv
    tool: docs/tools/booking-export.md
    check: python docs/tools/checks/csv-has-columns.py work/book.csv start service stylist
    on_fail: retry
    next: [hours]
  - id: hours
    needs: [book]
    produces: hours
    produce_path: work/hours.csv
    tool: docs/tools/hours-holiday-file.md
    check: python docs/tools/checks/file-exists.py work/hours.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [book, hours]
    produces: book-pack
    produce_path: out/book.md
    tool: docs/tools/booking-export.md
    check: python docs/tools/checks/file-exists.py out/book.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects this shop (**remember**).
