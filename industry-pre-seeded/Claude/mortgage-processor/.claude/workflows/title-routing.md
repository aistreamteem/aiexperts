# Title Routing

**When to use:** Index the title folder: commitment, updates, invoices, and related PDFs. Route names and dates. Do not clear exceptions. Do not hold money. Do not republish wire instructions. Do not give a title opinion. This is loan-file routing, not the real-estate transaction coordinator’s objection calendar. Draft stamps stay draft. Missing commitment stays missing. Write-up is a routing list plus missing schedules they named.

**How to run:** Open or continue a Work Item under `work-items/<id>/` using `continue` and `workflow-selector`. Copy `work-items/_TEMPLATE/` if the folder does not exist. Put source files in `in/`. Follow the steps below in order. Read each step's tool file under `docs/tools/`. Write artifacts at the YAML `produce_path` relative to the Work Item root (`work/` then `out/`). Run the step `check` from the Work Item root. Do not start a step whose `needs` files are missing. On check fail, retry at most three times, then ask with `operator-qa`. After each step, update the Work Item journal with `journal-keeper`. Human gate: label guesses; never declare CTC or a lock from a completed checklist. Completeness is not a lending decision.

**Initial phase:** `role-job`

## Work map

```yaml
id: title-routing
steps:
  - id: title
    needs: []
    produces: title
    produce_path: work/title-index.csv
    tool: docs/tools/title-folder.md
    check: python docs/tools/checks/csv-has-columns.py work/title-index.csv loan document
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [title]
    produces: title-pack
    produce_path: out/title-routing.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/title-routing.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects how *this* shop files.
