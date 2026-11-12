# Night Audit File Check

**When to use:** Check that the night-audit packet they dropped has the usual pages versus their PMS export: flash, occupancy, no-show, high-balance, exceptions. Name missing pages. Do not run audit or roll the date. Do not invent a flash total. Ask for a redacted file if PAN appears. They close the day. You deliver the completeness list and write-up. Trial versus final, if they drop both, stay labeled. High-balance folios already on the packet become exception pointers, not new amounts you invent.

**How to run:** Self-contained for **continue** / **workflow-selector**.

1. Confirm an active Work Item under `work-items/<id>/`. Put the night-audit packet and PMS export in `in/`.
2. Load `facts/MEMORY-INDEX.md`, then operations facts/rules, plus Work Item facts/rules if present.
3. Walk the steps below in order. Paths (`work/`, `out/`) are relative to `work-items/<id>/`. For each step: read the named tool doc, write the artifact, run the check. Missing needs → ask. Check fail → retry at most 3, then ask.
4. After the pack step, leave the finished list plus a short write-up in `out/` (docs used, artifacts, checks, open asks).
5. **journal-keeper**. One ready step per **continue** unless they asked for the whole named job.

**Initial phase:** `role-job`

## Work map

```yaml
id: night-audit-file-check
steps:
  - id: audit
    needs: []
    produces: audit
    produce_path: work/night-audit.pdf
    tool: docs/tools/night-audit-pdf.md
    check: python docs/tools/checks/file-exists.py work/night-audit.pdf
    on_fail: retry
    next: [pms]
  - id: pms
    needs: [audit]
    produces: pms
    produce_path: work/pms-house.csv
    tool: docs/tools/pms-export.md
    check: python docs/tools/checks/file-exists.py work/pms-house.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [audit, pms]
    produces: audit-pack
    produce_path: out/night-audit-file-check.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/night-audit-file-check.md
    on_fail: retry
    next: []
```

Starter step list. Replace tools and checks when they correct this property (**remember**).
