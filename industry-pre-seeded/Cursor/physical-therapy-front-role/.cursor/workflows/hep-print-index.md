# HEP print index

**When to use:** From their HEP library and the day list, list which charts have a therapist-attached or named HEP PDF ready to print. Do not pick a packet from the library as care. Do not write exercises. Do not coach. Missing named file stays a question. Filename and chart label are enough; do not paste exercise text into docs/. They print. You pack the index plus a write-up. Prefer chart number. One clinic date unless they asked otherwise.

**How to run:** Open or reuse `work-items/<id>/`. Put source files in `in/`. Follow this map in order: read the named `docs/tools/` file, write `produce_path` inside this Work Item, run the step `check`, retry at most 3 times on fail then ask. Pass produced files to the next step. One ready step per continue unless the operator asked for the whole job. Then journal-keeper.

**Initial phase:** `role-job`

## Work map

```yaml
id: hep-print-index
steps:
  - id: lib
    needs: []
    produces: hep
    produce_path: work/hep-index.csv
    tool: docs/tools/hep-pdf-library.md
    check: python docs/tools/checks/file-exists.py work/hep-index.csv
    on_fail: retry
    next: [day]
  - id: day
    needs: [hep]
    produces: day
    produce_path: work/day-list.csv
    tool: docs/tools/schedule-csv.md
    check: python docs/tools/checks/file-exists.py work/day-list.csv
    on_fail: retry
    next: [write]
  - id: write
    needs: [hep, day]
    produces: hep-writeup
    produce_path: out/hep-index.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/hep-index.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator confirms how this clinic works.
