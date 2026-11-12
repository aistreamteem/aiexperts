# CD and LE present

**When to use:** List Loan Estimate and Closing Disclosure versions in their LE/CD folder with issued dates as printed. Do not draft a disclosure. Do not invent a rate or a fee. Do not give a TRID legal opinion. Do not copy a full SSN. If lock file and CD disagree on rate, quote both after the lock file is in the pack. Write-up is a version list, not advice.

**How to run:** Open or continue a Work Item under `work-items/<id>/` using `continue` and `workflow-selector`. Copy `work-items/_TEMPLATE/` if the folder does not exist. Put source files in `in/`. Follow the steps below in order. Read each step's tool file under `docs/tools/`. Write artifacts at the YAML `produce_path` relative to the Work Item root (`work/` then `out/`). Run the step `check` from the Work Item root. Do not start a step whose `needs` files are missing. On check fail, retry at most three times, then ask with `operator-qa`. After each step, update the Work Item journal with `journal-keeper`. Human gate: label guesses; never declare CTC or a lock from a completed checklist. Completeness is not a lending decision.

**Initial phase:** `role-job`

## Work map

```yaml
id: cd-le-present
steps:
  - id: disc
    needs: []
    produces: disclosures
    produce_path: work/le-cd-index.csv
    tool: docs/tools/le-cd-pdf-folder.md
    check: python docs/tools/checks/csv-has-columns.py work/le-cd-index.csv loan document
    on_fail: retry
    next: [lock]
  - id: lock
    needs: [disclosures]
    produces: lock
    produce_path: work/lock-file.csv
    tool: docs/tools/lock-file.md
    check: python docs/tools/checks/file-exists.py work/lock-file.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [disclosures, lock]
    produces: disc-pack
    produce_path: out/cd-le-present.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/cd-le-present.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects how *this* shop files.
