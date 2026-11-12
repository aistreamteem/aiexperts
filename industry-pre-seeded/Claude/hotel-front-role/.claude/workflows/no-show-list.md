# No Show List

**When to use:** Build the no-show list from arrivals that did not check in and from the night-audit PDF if it already coded them. Fees follow their cancellation and guarantee policy only. Do not invent a charge or run a card. Cancelled rows are not no-shows. Group no-shows use the block file when it speaks. They post. You deliver the list and write-up.

**How to run:** Self-contained for **continue** / **workflow-selector**.

1. Confirm an active Work Item under `work-items/<id>/`. Put the arrivals export and night-audit PDF in `in/`.
2. Load `facts/MEMORY-INDEX.md`, then operations facts/rules, plus Work Item facts/rules if present.
3. Walk the steps below in order. Paths (`work/`, `out/`) are relative to `work-items/<id>/`. For each step: read the named tool doc, write the artifact, run the check. Missing needs → ask. Check fail → retry at most 3, then ask.
4. After the pack step, leave the finished list plus a short write-up in `out/` (docs used, artifacts, checks, open asks).
5. **journal-keeper**. One ready step per **continue** unless they asked for the whole named job.

**Initial phase:** `role-job`

## Work map

```yaml
id: no-show-list
steps:
  - id: arr
    needs: []
    produces: arrivals
    produce_path: work/arrivals.csv
    tool: docs/tools/arrivals-csv.md
    check: python docs/tools/checks/csv-has-columns.py work/arrivals.csv confirmation status
    on_fail: retry
    next: [audit]
  - id: audit
    needs: [arrivals]
    produces: audit
    produce_path: work/night-audit.pdf
    tool: docs/tools/night-audit-pdf.md
    check: python docs/tools/checks/file-exists.py work/night-audit.pdf
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [arrivals, audit]
    produces: noshow-pack
    produce_path: out/no-show-list.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/no-show-list.md
    on_fail: retry
    next: []
```

Starter step list. Replace tools and checks when they correct this property (**remember**).
