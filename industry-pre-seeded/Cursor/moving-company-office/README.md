# Moving company office — role Expert

This folder is an AI Expert for **moving company office** work: estimates from a rate file, inventories, crew-day lists, truck calendars, materials pulls, delivery windows, weigh-ticket packs, and claims as file routing, from rate sheets, inventories, scale tickets, and calendars you drop in.

- **Start:** `QUICK-START.md`
- **Role:** `MyRole.txt`
- **Method:** `docs/role/work-item-method.md`
- **Always-on instructions:** `AGENTS.md` and `.cursor/rules/expert.mdc`
- **Jobs:** `.cursor/workflows/` (registry in `workflow-registry.json`)
- **Memory:** `facts/facts-shared.md` and `facts/rules-shared.md`
- **Tools:** `docs/tools/`

Each real job is a Work Item under `work-items/<id>/` with `in/`, `work/`, `out/`, and `evidence/`. Do not mix Tuesday’s estimate with Monday’s crew day.

Starter facts and rules are typical US moving-office practice until you correct them for *this* shop.
