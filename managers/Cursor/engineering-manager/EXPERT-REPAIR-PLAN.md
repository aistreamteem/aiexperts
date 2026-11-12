# Repair plan for this Engineering Manager expert scaffold

**Applied to this Cursor Engineering Manager folder.** Paths use `.cursor/` and `AGENTS.md`. Fix 10 (developer HLD/DD skills) and the production-incident workflow do not apply here; this role already has charter/plan/escalation skills and team-delivery / team-escalation workflows. Vocabulary is management triggers, not SQL/git.

This folder was repaired by porting the completed Claude Engineering Manager repair (same plan) and adapting path/tool contracts for Cursor.

## Status

All applicable fixes from the original plan are applied:

| Group | Fixes | Notes |
| --- | --- | --- |
| A. Small code fixes | 1–6 | `.gitattributes`, `.gitignore`, bold field reader, template-based journal tests, table-based EM triggers, memory-optimize entry counting |
| B. One journal location | 7–9 | Skills/docs use `journals/work-items/<id>/`; legacy pointer is read-only fallback; stop/merge/audit hooks are Python on the real journal |
| C. Content | 11–12 (10 N/A) | Shared memory pair; leftovers cleaned; `AGENTS.md` matches skills. No HLD/DD skills or production-incident workflow for this role |
| D. Keeping it fixed | 13 | `scripts/check_scaffold.py` plus hook test scripts |
