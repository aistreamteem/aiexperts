# Medical clinic front role Expert

Role Expert for **Medical clinic front role (not the clinician)**. Paperwork and lists from files you drop in — not clinical care.

- Start: `QUICK-START.md`
- Role: `MyRole.txt`
- Method: `docs/role/work-item-method.md`
- Instructions: `CLAUDE.md`
- Memory: shared (`facts/facts-shared.md`, `facts/rules-shared.md`) then operations (`facts/facts-operations.md`, `facts/rules-operations.md`)
- Jobs: `.claude/workflows/` (registry: `workflow-registry.json`)
- Tools: `docs/tools/`

Each appointment, clinic date, or pack is a Work Item under `work-items/<id>/` with `in/`, `work/`, `out/`, and `evidence/`. Journals live under `journals/`.
