# Physical therapy front role — role Expert

This folder is an AI Expert for **physical therapy front role** work (not the therapist): day lists, remaining visits from their files, referral and plan-of-care completeness, recert dates, HEP print indexes, no-show and wait-list packs, and day-close, from EHR exports and folders you drop in.

- **Start:** `QUICK-START.md`
- **Role:** `MyRole.txt`
- **Method:** `docs/role/work-item-method.md`
- **Always-on instructions:** `CLAUDE.md` and `.claude/rules/expert.md`
- **Jobs:** `.claude/workflows/` (registry in `workflow-registry.json`)
- **Memory:** shared (`facts/facts-shared.md`, `facts/rules-shared.md`) plus operations (`facts/facts-operations.md`, `facts/rules-operations.md`)
- **Tools:** `docs/tools/`

Each real job is a Work Item under `work-items/<id>/` with `in/`, `work/`, `out/`, and `evidence/`. Do not mix Tuesday’s day list with Monday’s remaining-visits pack.

Starter facts and rules are typical US outpatient PT front-role practice until you correct them for *this* clinic.
