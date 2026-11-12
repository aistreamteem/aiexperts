# Facilities / plant maintenance planner — role Expert

This folder is an AI Expert for **facilities / plant maintenance planner** work: work-order dispatch lists, PM-due lists, parts-below-min packs, backlog, downtime, LOTO-present indexes, contractor WO lists, and warranty-due lists as files, from CMMS exports, crib sheets, and procedure PDFs you drop in.

- **Start:** `QUICK-START.md`
- **Role:** `MyRole.txt`
- **Method:** `docs/role/work-item-method.md`
- **Always-on instructions:** `AGENTS.md` and `.cursor/rules/expert.mdc`
- **Jobs:** `.cursor/workflows/` (registry in `workflow-registry.json`)
- **Memory:** `facts/facts-operations.md` and `facts/rules-operations.md`
- **Tools:** `docs/tools/`

Each real job is a Work Item under `work-items/<id>/` with `in/`, `work/`, `out/`, and `evidence/`. Do not mix Tuesday’s dispatch board with Monday’s PM-due list.

Starter facts and rules are typical US in-house maintenance-planner practice until you correct them for *this* plant.
