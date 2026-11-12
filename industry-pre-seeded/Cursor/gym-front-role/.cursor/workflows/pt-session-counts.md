# PT session counts

**When to use:** Tabulate purchased, used, and remaining PT sessions from their package sheet. Join the membership export so plan and status stay attached. Do not invent remaining punches or a complimentary session. No-show burns a session only if their file coded it that way. You do not write a training plan. Produce the count sheet plus a pack note. They train and they decide comps. Starter until they teach this club’s decrement rule.

**How to run:** Open or continue the Work Item under `work-items/<id>/`. Follow this file's YAML via **continue**. Read the cited `docs/tools/` doc, write artifacts under the Work Item, run the step `check`, store logs in `evidence/`, then **journal-keeper**.

**Initial phase:** `role-job`

## Work map

```yaml
id: pt-session-counts
steps:
  - id: pt
    needs: []
    produces: sessions
    produce_path: work/pt-sessions.csv
    tool: docs/tools/pt-package-sheet.md
    check: python docs/tools/checks/csv-has-columns.py work/pt-sessions.csv member_id remaining
    on_fail: retry
    next: [members]
  - id: members
    needs: [sessions]
    produces: members
    produce_path: work/membership.csv
    tool: docs/tools/membership-export.md
    check: python docs/tools/checks/file-exists.py work/membership.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [sessions, members]
    produces: pt-pack
    produce_path: out/pt-session-counts.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/pt-session-counts.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects this shop.
