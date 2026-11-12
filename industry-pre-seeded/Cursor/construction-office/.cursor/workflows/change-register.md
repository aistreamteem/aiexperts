# Change Register

**When to use:** Open potential changes and signed change orders from their register. No pricing by this Expert. Keep their names such as PCO, COR, or CO. Do not create a number or say a ticket is billable. Verbal extras stay flagged as missing written follow-up when that is their rule. Directed-change papers are listed if they are on the register, not upgraded to a signed CO. The pack quotes status and amounts as printed and asks where notice dates are blank.

**How to run:** Follow `docs/role/work-item-method.md`. Use or create `work-items/<id>/`. Put source files in `in/`. For each YAML step below, in order: (1) do not start if `needs` files are missing — ask the operator; (2) read the `tool` file under `docs/tools/`; (3) write `produce_path` inside this Work Item folder (`work/` and `out/` are relative to the Work Item, not the expert root); (4) run `check` with those same relative paths; (5) on fail, retry at most 3 times then ask via **operator-qa**; (6) update the Work Item journal with **journal-keeper**. After the last step, the pack in `out/` must quote their source files. Do not invent counts, dates, approvals, or answers.

**Initial phase:** `intake`

## Work map

```yaml
id: change-register
steps:
  - id: list
    needs: []
    produces: pco-raw
    produce_path: work/pco-register.csv
    tool: docs/tools/procore-pattern.md
    check: python docs/tools/checks/csv-has-columns.py work/pco-register.csv number status
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [pco-raw]
    produces: pco-pack
    produce_path: out/change-register.md
    tool: docs/tools/procore-pattern.md
    check: python docs/tools/checks/file-exists.py out/change-register.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they confirm how this shop files.
