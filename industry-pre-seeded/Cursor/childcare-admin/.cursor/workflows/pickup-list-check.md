# Pickup authorization check

**When to use:** Compare the live pickup list to the roster and to any sign-out adults they exported. Flag an adult who is not on the authorization page. Emergency contacts are not pickup people unless their form says so. You never release a child and you never interpret a court order — say order on file only if they stored one. Door codes stay out. Ask the director on every mismatch. Photo-ID images do not belong in docs/.

**How to run:** Self-contained. Confirm an active Work Item at `work-items/<id>/` (copy `work-items/_TEMPLATE/` if needed). Paths `in/`, `work/`, `out/`, and `evidence/` are inside that folder. Load operations memory, then walk the map: a step is ready when every `needs` artifact exists on disk. Read the named `docs/tools/` file, produce `produce_path`, run `check` from the Work Item folder. On fail, retry at most 3 times, then ask with **operator-qa**. Do not invent a pass. After each step, **journal-keeper**. One ready step per **continue** unless the operator asked for the whole job. Finished pack lands in `out/`. Director gates (start, release, signatures) are not skipped.

**Initial phase:** `role-job`

## Work map

```yaml
id: pickup-list-check
steps:
  - id: auth
    needs: []
    produces: auth
    produce_path: work/pickup.csv
    tool: docs/tools/pickup-list.md
    check: python docs/tools/checks/csv-has-columns.py work/pickup.csv child adult
    on_fail: retry
    next: [roster]
  - id: roster
    needs: [auth]
    produces: roster
    produce_path: work/roster.csv
    tool: docs/tools/roster-sheet.md
    check: python docs/tools/checks/file-exists.py work/roster.csv
    on_fail: retry
    next: [write]
  - id: write
    needs: [auth, roster]
    produces: pickup-pack
    produce_path: out/pickup-check.md
    tool: docs/tools/pickup-list.md
    check: python docs/tools/checks/file-exists.py out/pickup-check.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects them through **remember**.
