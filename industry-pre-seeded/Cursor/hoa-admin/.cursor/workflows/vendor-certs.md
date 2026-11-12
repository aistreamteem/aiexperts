# Vendor Certs

**When to use:** List expiration dates, named insured, and additional-insured wording as printed from certificates they filed. Not a coverage opinion. Flag expired dates, wrong community names, and missing lines their checklist requires for staff. Do not store producer logins. One vendor per row unless they asked for a certificate-aging index. Produce the CSV the checks can see, then the write-up. Confirm the association name on each certificate before you flag a date.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put operator files in `in/`. Walk the YAML steps below in order (one ready step per **continue** unless the operator asked for the whole named job). For each step: read the cited tool doc under `docs/tools/`, write the produced file under this Work Item (`work/` or `out/`), run the listed check against those same paths, copy check logs to `evidence/`, then update the Work Item journal with **journal-keeper**. Do not start a step whose `needs` files are missing. On check fail, retry the same step at most three times, then record the blocker and ask the operator. Human gates in `docs/role/work-item-method.md` are not passed by the word continue.

**Initial phase:** `role-job`

## Work map

```yaml
id: vendor-certs
steps:
  - id: index
    needs: []
    produces: coi-raw
    produce_path: work/vendor-certs.csv
    tool: docs/tools/vendor-coi.md
    check: python docs/tools/checks/file-exists.py work/vendor-certs.csv
    on_fail: retry
    next: [write]
  - id: write
    needs: [coi-raw]
    produces: coi-writeup
    produce_path: out/vendor-certs.md
    tool: docs/tools/vendor-coi.md
    check: python docs/tools/checks/file-exists.py out/vendor-certs.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator **remember**s how this shop actually files.
