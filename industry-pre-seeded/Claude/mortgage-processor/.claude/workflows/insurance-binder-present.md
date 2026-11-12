# Insurance Binder Present

**When to use:** List HOI binders, dec pages, master policies, and flood policies in their insurance-binder folder. Copy effective dates and mortgagee line as printed. Do not bind. Do not invent a limit. Do not say they are covered. Flood and HOI stay separate. Quote versus binder stay labeled. Expired dates stay flagged. Write-up is present-missing plus date flags, not a coverage opinion.

**How to run:** Open or continue a Work Item under `work-items/<id>/` using `continue` and `workflow-selector`. Copy `work-items/_TEMPLATE/` if the folder does not exist. Put source files in `in/`. Follow the steps below in order. Read each step's tool file under `docs/tools/`. Write artifacts at the YAML `produce_path` relative to the Work Item root (`work/` then `out/`). Run the step `check` from the Work Item root. Do not start a step whose `needs` files are missing. On check fail, retry at most three times, then ask with `operator-qa`. After each step, update the Work Item journal with `journal-keeper`. Human gate: label guesses; never declare CTC or a lock from a completed checklist. Completeness is not a lending decision.

**Initial phase:** `role-job`

## Work map

```yaml
id: insurance-binder-present
steps:
  - id: ins
    needs: []
    produces: insurance
    produce_path: work/insurance-index.csv
    tool: docs/tools/insurance-binder-folder.md
    check: python docs/tools/checks/csv-has-columns.py work/insurance-index.csv loan document
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [insurance]
    produces: insurance-pack
    produce_path: out/insurance-binder-present.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/insurance-binder-present.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects how *this* shop files.
