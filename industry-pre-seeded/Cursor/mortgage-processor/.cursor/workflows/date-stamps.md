# Date-stamp pack

**When to use:** Build a date-file pack from their calendar and document-folder index: application, VOE as-of, stub period-end, LE issued, CD issued, lock expiration, and closing as they stored them. Quote the source file for each date. Do not invent a date. Do not decide TRID waits as counsel. Do not lock. Do not store a full SSN. Write-up lists dates and blanks, not a legal timeline opinion.

**How to run:** Open or continue a Work Item under `work-items/<id>/` using `continue` and `workflow-selector`. Copy `work-items/_TEMPLATE/` if the folder does not exist. Put source files in `in/`. Follow the steps below in order. Read each step's tool file under `docs/tools/`. Write artifacts at the YAML `produce_path` relative to the Work Item root (`work/` then `out/`). Run the step `check` from the Work Item root. Do not start a step whose `needs` files are missing. On check fail, retry at most three times, then ask with `operator-qa`. After each step, update the Work Item journal with `journal-keeper`. Human gate: label guesses; never declare CTC or a lock from a completed checklist. Completeness is not a lending decision.

**Initial phase:** `role-job`

## Work map

```yaml
id: date-stamps
steps:
  - id: cal
    needs: []
    produces: calendar
    produce_path: work/processor-calendar.csv
    tool: docs/tools/calendar.md
    check: python docs/tools/checks/csv-has-columns.py work/processor-calendar.csv loan date
    on_fail: retry
    next: [index]
  - id: index
    needs: [calendar]
    produces: index
    produce_path: work/document-index.csv
    tool: docs/tools/document-folder-index.md
    check: python docs/tools/checks/file-exists.py work/document-index.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [calendar, index]
    produces: dates
    produce_path: out/date-stamps.md
    tool: docs/tools/calendar.md
    check: python docs/tools/checks/file-exists.py out/date-stamps.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects how *this* shop files.
