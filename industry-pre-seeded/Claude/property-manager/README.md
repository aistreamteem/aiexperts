# Property manager write-ups — role Expert

This folder is an AI Expert for **property manager write-ups**: work orders, make-ready lists, rent-roll files, vendor quotes, deposit ledgers, owner packs, and notice-process lists as files, from PMS exports and PDFs you drop in.

- **Start:** `QUICK-START.md`
- **Role:** `MyRole.txt`
- **Method:** `docs/role/work-item-method.md`
- **Always-on instructions:** `CLAUDE.md` and `.claude/rules/expert.md`
- **Jobs:** `.claude/workflows/` (registry in `workflow-registry.json`)
- **Memory:** `facts/facts-shared.md` and `facts/rules-shared.md`
- **Tools:** `docs/tools/`

Each real job is a Work Item under `work-items/<id>/` with `in/`, `work/`, `out/`, and `evidence/`. Do not mix Tuesday’s work-order export with last month’s owner pack.

Starter facts and rules are typical US property-management-office practice until you correct them for *this* shop.
