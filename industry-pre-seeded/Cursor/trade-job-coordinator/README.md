# Job coordinator in a trade shop — role Expert

This folder is an AI Expert for **job coordinator** work in a field trade office (HVAC, plumbing, electrical, similar): dispatch board, parts and packing lists, callbacks, permit numbers on file, and closeout photo packs, from schedule exports and PDFs you drop in.

- **Start:** `QUICK-START.md`
- **Role:** `MyRole.txt`
- **Method:** `docs/role/work-item-method.md`
- **Always-on instructions:** `AGENTS.md` and `.cursor/rules/expert.mdc`
- **Jobs:** `.cursor/workflows/` (registry in `workflow-registry.json`)
- **Memory:** `facts/facts-operations.md` and `facts/rules-operations.md`
- **Tools:** `docs/tools/`

Each real job is a Work Item under `work-items/<id>/` with `in/`, `work/`, `out/`, and `evidence/`. Do not mix Tuesday’s ticket with Monday’s day-board.

Starter facts and rules are typical US trade-shop dispatch practice until you correct them for *this* shop.
