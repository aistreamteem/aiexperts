# Auth Gap

**When to use:** Compare estimate lines to the authorization log on the RO or export. List pending lines and additional findings that still need who, when, and amount, or their digital approve. Do not mark those lines sold. Fleet PO and warranty claim blanks are gaps when their process requires them. Independent and dealer tickets both hide extras in the bay; the pack makes the gap visible. You do not call the customer. You do not invent a phone approval. Invoice extras belong on the pickup check, not as silent sold work here.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Follow the YAML steps in order: read the named tool doc under `docs/tools/`, write `produce_path` inside this Work Item (`work/` and `out/` mean `work-items/<id>/work/` and `work-items/<id>/out/`), run the listed check against those same paths, then **journal-keeper**. Do not start a step whose `needs` files are missing. On check fail, retry at most three times, then ask. `continue` walks one ready step unless the operator asked for the whole job.

**Initial phase:** `role-job`

## Work map

```yaml
id: auth-gap
steps:
  - id: pull
    needs: []
    produces: auth-raw
    produce_path: work/auth-lines.csv
    tool: docs/tools/shop-sw.md
    check: python docs/tools/checks/csv-has-columns.py work/auth-lines.csv ro line auth
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [auth-raw]
    produces: auth-pack
    produce_path: out/auth-gaps.md
    tool: docs/tools/ro-pdf.md
    check: python docs/tools/checks/file-exists.py out/auth-gaps.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects this shop's process (**remember**).
