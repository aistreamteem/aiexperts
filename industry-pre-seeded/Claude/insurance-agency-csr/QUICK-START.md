# Insurance agency CSR (not the producer) — role Expert

This folder is an AI Expert for **independent-agency CSR** work: certificate requests, expiration and renewal lists, ACORD completeness, FNOL routing, and policy-change paperwork as files, from AMS exports and PDFs you drop in.

- **Start:** `QUICK-START.md`
- **Role:** `MyRole.txt`
- **Method:** `docs/role/work-item-method.md`
- **Always-on instructions:** `CLAUDE.md` and `.claude/rules/expert.mdc`
- **Jobs:** `.claude/workflows/` (registry in `workflow-registry.json`)
- **Memory:** `facts/facts-operations.md` and `facts/rules-operations.md`
- **Tools:** `docs/tools/`

Each real job is a Work Item under `work-items/<id>/` with `in/`, `work/`, `out/`, and `evidence/`. Do not mix Tuesday’s COI with Monday’s expiration list.

Starter facts and rules are typical US independent-agency CSR practice until you correct them for *this* shop.
