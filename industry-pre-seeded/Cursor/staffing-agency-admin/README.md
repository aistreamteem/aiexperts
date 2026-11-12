# Staffing agency office admin — role Expert

This folder is an AI Expert for **staffing agency office admin** work: assignment boards, credential-date lists, job-order completeness, orientation-missing lists, DNS/DNR lists, holiday-shift lists, incident routing, and timesheet-completeness packs as files, from sheets, rate files, and PDFs you drop in.

- **Start:** `QUICK-START.md`
- **Role:** `MyRole.txt`
- **Method:** `docs/role/work-item-method.md`
- **Always-on instructions:** `AGENTS.md` and `.cursor/rules/expert.mdc`
- **Jobs:** `.cursor/workflows/` (registry in `workflow-registry.json`)
- **Memory:** `facts/facts-shared.md` and `facts/rules-shared.md`
- **Tools:** `docs/tools/`

Each real job is a Work Item under `work-items/<id>/` with `in/`, `work/`, `out/`, and `evidence/`. Do not mix Tuesday’s timesheets with Monday’s assignment board.

Starter facts and rules are typical US staffing-office practice until you correct them for *this* shop.
