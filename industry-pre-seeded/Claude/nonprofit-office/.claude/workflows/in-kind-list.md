# In Kind List

**When to use:** List in-kind rows from their log: date, donor label, description they wrote, program tag. No fair-market values and no wage for time. Point unusual items (vehicles, real estate, art, crypto) at their gift-acceptance policy and stop. Do not complete an appraisal or tell the donor what to deduct. Volunteer hours stay on the volunteer log unless their files already treat hours as in-kind. Blank descriptions are questions, not rows you finish from a photo guess. Output is the working log extract and a pack note of holes. They accept gifts. You list.

**How to run:** Follow this file with **continue**. Paths `work/` and `out/` mean inside `work-items/<id>/`. Load `facts/MEMORY-INDEX.md` then shared facts/rules. If no Work Item exists, use **workflow-selector** for this job and copy `work-items/_TEMPLATE/`. Put operator files in `in/`. For each ready YAML step: read its tool doc; do not start if `needs` files are missing; write `produce_path`; run `check` against this Work Item’s paths (retry at most three times, then ask). Pass produced files to later steps. Missing shop knowledge → **operator-qa** or ask; do not invent. After the last check passes, the pack is `out/` plus `STATUS.md` (sources, artifacts, check results). They circulate, sign, send, submit, or talk to donors — you do not. **journal-keeper** after the step (or after the whole named job if they asked for the whole job).

**Initial phase:** `role-job`

## Steps

1. Extract the in-kind log (docs/tools/in-kind-log.md) → `work/inkind.csv`.
2. List rows and holes without FMV or wages → `out/inkind.md`. They accept gifts. You list.

## Work map

```yaml
id: in-kind-list
steps:
  - id: pull
    needs: []
    produces: inkind
    produce_path: work/inkind.csv
    tool: docs/tools/in-kind-log.md
    check: python docs/tools/checks/file-exists.py work/inkind.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [inkind]
    produces: inkind-out
    produce_path: out/inkind.md
    tool: docs/tools/in-kind-log.md
    check: python docs/tools/checks/file-exists.py out/inkind.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when this shop corrects them.
