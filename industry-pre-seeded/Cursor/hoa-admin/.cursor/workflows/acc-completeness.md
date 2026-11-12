# ACC Completeness

**When to use:** List missing pages, sketches, neighbor notes, and unsigned fields on the architectural application they use, against their form or guidelines. Not an approval or denial and not a committee stamp. A lot that does not match the roster is a question. One application per row unless they asked for a batch completeness list. Produce the CSV the checks can see, then the write-up.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put operator files in `in/`. Walk the YAML steps below in order (one ready step per **continue** unless the operator asked for the whole named job). For each step: read the cited tool doc under `docs/tools/`, write the produced file under this Work Item (`work/` or `out/`), run the listed check against those same paths, copy check logs to `evidence/`, then update the Work Item journal with **journal-keeper**. Do not start a step whose `needs` files are missing. On check fail, retry the same step at most three times, then record the blocker and ask the operator. Human gates in `docs/role/work-item-method.md` are not passed by the word continue.

**Initial phase:** `role-job`

## Work map

```yaml
id: acc-completeness
steps:
  - id: list
    needs: []
    produces: acc-raw
    produce_path: work/acc-forms.csv
    tool: docs/tools/acc-form.md
    check: python docs/tools/checks/file-exists.py work/acc-forms.csv
    on_fail: retry
    next: [write]
  - id: write
    needs: [acc-raw]
    produces: acc-writeup
    produce_path: out/acc-check.md
    tool: docs/tools/acc-form.md
    check: python docs/tools/checks/file-exists.py out/acc-check.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator **remember**s how this shop actually files.
