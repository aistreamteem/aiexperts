# One RO

**When to use:** One ticket write-up: concern in customer words, vehicle fields from their RO, parts file from confirmations, estimate questions from their labor matrix. Cause and correction only if the tech file has them. No invented diagnosis, VIN, book time, or auth. Keep declined lines. MPI only from their form. Phone approval only from their log. Independent and dealer packs follow the same completeness idea. Ask when a needed file is missing rather than filling the three C's from memory.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Follow the YAML steps in order: read the named tool doc under `docs/tools/`, write `produce_path` inside this Work Item (`work/` and `out/` mean `work-items/<id>/work/` and `work-items/<id>/out/`), run the listed check against those same paths, then **journal-keeper**. Do not start a step whose `needs` files are missing. On check fail, retry at most three times, then ask. `continue` walks one ready step unless the operator asked for the whole job.

**Initial phase:** `role-job`

## Work map

```yaml
id: one-ro
steps:
  - id: parts
    needs: []
    produces: ro-parts
    produce_path: work/ro-parts.csv
    tool: docs/tools/parts-counter.md
    check: python docs/tools/checks/csv-has-columns.py work/ro-parts.csv part status
    on_fail: retry
    next: [notes]
  - id: notes
    needs: [ro-parts]
    produces: ro-notes
    produce_path: work/ro-notes.md
    tool: docs/tools/ro-pdf.md
    check: python docs/tools/checks/file-exists.py work/ro-notes.md
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [ro-notes]
    produces: ro-writeup
    produce_path: out/ro-writeup.md
    tool: docs/tools/ro-pdf.md
    check: python docs/tools/checks/file-exists.py out/ro-writeup.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects this shop's process (**remember**).
