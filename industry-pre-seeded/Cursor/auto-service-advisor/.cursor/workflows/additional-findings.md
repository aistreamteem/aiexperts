# Additional Findings

**When to use:** New technician or MPI recommendations not yet authorized. Plain-language list with their labor-matrix and parts prices. Do not mark sold. Keep the original concern first. Declined items stay declined if already decided. Independent waiters and dealer warranty cars still need who, when, and amount. You do not diagnose and you do not say the finding is legally required. Missing prices are questions. OEM versus aftermarket is the quality word on their quote, not a safety ruling. You do not send the customer message.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Follow the YAML steps in order: read the named tool doc under `docs/tools/`, write `produce_path` inside this Work Item (`work/` and `out/` mean `work-items/<id>/work/` and `work-items/<id>/out/`), run the listed check against those same paths, then **journal-keeper**. Do not start a step whose `needs` files are missing. On check fail, retry at most three times, then ask. `continue` walks one ready step unless the operator asked for the whole job.

**Initial phase:** `role-job`

## Work map

```yaml
id: additional-findings
steps:
  - id: find
    needs: []
    produces: find-raw
    produce_path: work/findings.csv
    tool: docs/tools/mpi-form.md
    check: python docs/tools/checks/csv-has-columns.py work/findings.csv item price auth
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [find-raw]
    produces: findings-pack
    produce_path: out/additional-findings.md
    tool: docs/tools/shop-sw.md
    check: python docs/tools/checks/file-exists.py out/additional-findings.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects this shop's process (**remember**).
