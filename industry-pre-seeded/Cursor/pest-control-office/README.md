# Pest control office — role Expert

This folder is an AI Expert for **pest control office** work: route-day lists, skip lists, callback lists, chemical-log completeness, inventory vs log, bait-map indexes, device counts, price-file estimates, and WDO form packs, from sheets and PDFs you drop in.

- **Start:** `QUICK-START.md`
- **Role:** `MyRole.txt`
- **Method:** `docs/role/work-item-method.md`
- **Always-on instructions:** `AGENTS.md` and `.cursor/rules/expert.mdc`
- **Jobs:** `.cursor/workflows/` (registry in `workflow-registry.json`)
- **Memory:** `facts/facts-operations.md` and `facts/rules-operations.md`
- **Tools:** `docs/tools/`

Each real job is a Work Item under `work-items/<id>/` with `in/`, `work/`, `out/`, and `evidence/`. Do not mix Tuesday’s route with Monday’s callback list.

Starter facts and rules are typical US pest-office practice until you correct them for *this* shop.
