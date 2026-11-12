# MPI Pack

**When to use:** Copy red, yellow, green, or their tags and photo captions from their inspection export only. Not a state inspection and not a pass sticker. Do not invent a 50-point list. Recommendations need their prices before they go to a findings call, and they stay unsold without auth. Describe only attached photos. A caption is not a diagnosis unless the tech wrote one. Independent DVI and dealer factory MPI both count. Missing export means ask. Do not say the car is safe because boxes are green.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Follow the YAML steps in order: read the named tool doc under `docs/tools/`, write `produce_path` inside this Work Item (`work/` and `out/` mean `work-items/<id>/work/` and `work-items/<id>/out/`), run the listed check against those same paths, then **journal-keeper**. Do not start a step whose `needs` files are missing. On check fail, retry at most three times, then ask. `continue` walks one ready step unless the operator asked for the whole job.

**Initial phase:** `role-job`

## Work map

```yaml
id: mpi-pack
steps:
  - id: pull
    needs: []
    produces: mpi-raw
    produce_path: work/mpi.csv
    tool: docs/tools/mpi-form.md
    check: python docs/tools/checks/csv-has-columns.py work/mpi.csv item rating
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [mpi-raw]
    produces: mpi-pack
    produce_path: out/mpi.md
    tool: docs/tools/mpi-form.md
    check: python docs/tools/checks/file-exists.py out/mpi.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects this shop's process (**remember**).
