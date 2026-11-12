# Chemical Log Completeness

**When to use:** List application-log rows and flag blanks they use: product, EPA-from-their-file, rate-as-logged, tech, interior versus exterior. Do not invent a mix, rate, or EPA number. Tickets that say treated with no log row stay holes. License-on-file is present-or-missing, not a stamp. Held wind stops do not get a fake row. They complete the log. You write the hole list and a write-up the check can see.

## How to run

This file is the whole job. **continue** and **workflow-selector** walk it. Do not look for deleted process skills.

1. Confirm or open a Work Item under `work-items/<id>/` (use **workflow-selector** if none is active). Record this job id as the workflow type.
2. Load `facts/MEMORY-INDEX.md`, then `facts/facts-operations.md` and `facts/rules-operations.md`. Load Work Item facts/rules if present.
3. Put operator files in `work-items/<id>/in/`. Working extracts go in `work-items/<id>/work/`. Finished packs go in `work-items/<id>/out/`. Check logs go in `work-items/<id>/evidence/`.
4. Read only the tool docs named on each step.
5. Walk steps in order. Rewrite every `work/` and `out/` path so it sits under the Work Item folder. Do not start a step whose `needs` files are missing — ask.
6. After each step, run the listed check from the expert root with those rewritten paths. The step passes only when the check exits 0. On fail, retry at most 3 times, then ask. If a step has no check, propose a check and get operator approval before marking it passed.
7. Update the Work Item journal with **journal-keeper**. Missing shop knowledge: ask; do not invent. Requests outside `MyRole.txt`: refuse and stop.

**Initial phase:** `role-job`

## Work map

```yaml
id: chemical-log-completeness
steps:
  - id: log
    needs: []
    produces: log
    produce_path: work/chemical-log.csv
    tool: docs/tools/chemical-log.md
    check: python docs/tools/checks/csv-has-columns.py work/chemical-log.csv date account
    on_fail: retry
    next: [tickets]
  - id: tickets
    needs: [log]
    produces: tickets
    produce_path: work/log-tickets.csv
    tool: docs/tools/ticket-sheet.md
    check: python docs/tools/checks/file-exists.py work/log-tickets.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [log, tickets]
    produces: log-pack
    produce_path: out/chemical-log-completeness.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/chemical-log-completeness.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this shop.
