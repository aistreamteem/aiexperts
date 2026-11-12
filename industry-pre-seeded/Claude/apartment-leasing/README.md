# Apartment leasing admin — role Expert

This folder is an AI Expert for **apartment leasing admin** work: guest cards, showings, application completeness, lease-packet checklists, and move-in dates as files, from PMS exports and PDFs you drop in.

- **Start:** `QUICK-START.md`
- **Role:** `MyRole.txt`
- **Method:** `docs/role/work-item-method.md`
- **Always-on instructions:** `CLAUDE.md` and `.claude/rules/expert.md`
- **Jobs:** `.claude/workflows/` (registry in `workflow-registry.json`)
- **Memory:** `facts/facts-shared.md` and `facts/rules-shared.md`
- **Tools:** `docs/tools/`

Each real job is a Work Item under `work-items/<id>/` with `in/`, `work/`, `out/`, and `evidence/`. Do not mix Tuesday’s application with Monday’s showing list.

Starter facts and rules are typical US leasing-admin practice until you correct them for *this* shop.
