# Donor List

**When to use:** Filter the donor export they provided. List holes: missing fund or restriction code, missing acknowledgment flag, pledges mixed with cash, duplicate IDs. They communicate. No email, SMS, or CRM blast. Do not mark sent because you drafted a letter. Soft credit stays as their sheet defines it; do not move hard credit. Least PII in the pack note. Output is the working CSV and a list they can use in their own tools. Segmentation is a filter, not a send. Employer-stack messaging is out of scope.

**How to run:** Follow this file with **continue**. Paths `work/` and `out/` mean inside `work-items/<id>/`. Load `facts/MEMORY-INDEX.md` then shared facts/rules. If no Work Item exists, use **workflow-selector** for this job and copy `work-items/_TEMPLATE/`. Put operator files in `in/`. For each ready YAML step: read its tool doc; do not start if `needs` files are missing; write `produce_path`; run `check` against this Work Item’s paths (retry at most three times, then ask). Pass produced files to later steps. Missing shop knowledge → **operator-qa** or ask; do not invent. After the last check passes, the pack is `out/` plus `STATUS.md` (sources, artifacts, check results). They circulate, sign, send, submit, or talk to donors — you do not. **journal-keeper** after the step (or after the whole named job if they asked for the whole job).

**Initial phase:** `role-job`

## Steps

1. Filter the donor export they provided (docs/tools/donor-csv.md) → `work/donors.csv`.
2. List holes (missing fund, ack flag, mixed pledges) → `out/donor-list.md`. They communicate. You do not send.

## Work map

```yaml
id: donor-list
steps:
  - id: pull
    needs: []
    produces: donors
    produce_path: work/donors.csv
    tool: docs/tools/donor-csv.md
    check: python docs/tools/checks/csv-has-columns.py work/donors.csv date amount
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [donors]
    produces: donor-out
    produce_path: out/donor-list.md
    tool: docs/tools/donor-csv.md
    check: python docs/tools/checks/file-exists.py out/donor-list.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when this shop corrects them.
