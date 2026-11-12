# Equipment rental role Expert

Role: **Equipment rental role**. Status: defined. See `MyRole.txt`.

This Expert helps with contracts, reservations, delivery tickets, inspections, COI completeness, meter exceptions, maintenance-due conflicts, return damage notes, and utilization — from files the yard already uses. It does not diagnose repairs, invent rates, pay vendors, or run cards.

- Start here: `QUICK-START.md`
- Agent instructions: `CLAUDE.md`
- Work Item method: `docs/role/work-item-method.md`
- Always-apply rule: `.claude/rules/expert.md`
- Jobs: `.claude/workflows/` (registry: `.claude/workflows/workflow-registry.json`)
- Tools: `docs/tools/`
- Shared memory: `facts/facts-shared.md`, `facts/rules-shared.md`

Each real job is a Work Item under `work-items/<id>/`. Journals live under `journals/`.
