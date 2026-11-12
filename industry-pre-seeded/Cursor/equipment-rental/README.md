# Equipment rental role Expert

Role: **Equipment rental role**. Status: defined. See `MyRole.txt`.

This Expert helps with contracts, reservations, delivery tickets, inspections, COI completeness, meter exceptions, maintenance-due conflicts, return damage notes, and utilization — from files the yard already uses. It does not diagnose repairs, invent rates, pay vendors, or run cards.

- Start here: `QUICK-START.md`
- Agent instructions: `AGENTS.md`
- Work Item method: `docs/role/work-item-method.md`
- Always-apply rule: `.cursor/rules/expert.mdc`
- Jobs: `.cursor/workflows/` (registry: `.cursor/workflows/workflow-registry.json`)
- Tools: `docs/tools/`
- Operations memory: `facts/facts-operations.md`, `facts/rules-operations.md`

Each real job is a Work Item under `work-items/<id>/`. Journals live under `journals/`.
