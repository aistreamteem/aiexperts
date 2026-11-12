# Weekly Minutes

**When to use:** Agenda plus open actions from last minutes they filed. They send anything to people. Extract only numbered actions with owners and dates they recorded. Do not add implied work or speak for the owner. Unsigned minutes, if they track approval, stay marked unsigned. This week's agenda topics come from their template or notes, not from a starter list you invent. The pack names the minutes file and keeps action rows the check can see so the next meeting starts from their record.

**How to run:** Follow `docs/role/work-item-method.md`. Use or create `work-items/<id>/`. Put source files in `in/`. For each YAML step below, in order: (1) do not start if `needs` files are missing — ask the operator; (2) read the `tool` file under `docs/tools/`; (3) write `produce_path` inside this Work Item folder (`work/` and `out/` are relative to the Work Item, not the expert root); (4) run `check` with those same relative paths; (5) on fail, retry at most 3 times then ask via **operator-qa**; (6) update the Work Item journal with **journal-keeper**. After the last step, the pack in `out/` must quote their source files. Do not invent counts, dates, approvals, or answers.

**Initial phase:** `intake`

## Work map

```yaml
id: weekly-minutes
steps:
  - id: agenda
    needs: []
    produces: agenda-raw
    produce_path: work/meeting-agenda.csv
    tool: docs/tools/meeting-minutes.md
    check: python docs/tools/checks/csv-has-columns.py work/meeting-agenda.csv topic owner
    on_fail: retry
    next: [actions]
  - id: actions
    needs: [agenda-raw]
    produces: actions-raw
    produce_path: work/meeting-actions.csv
    tool: docs/tools/meeting-minutes.md
    check: python docs/tools/checks/csv-has-columns.py work/meeting-actions.csv action owner
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [actions-raw]
    produces: meet-pack
    produce_path: out/meeting-pack.md
    tool: docs/tools/meeting-minutes.md
    check: python docs/tools/checks/file-exists.py out/meeting-pack.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they confirm how this shop files.
