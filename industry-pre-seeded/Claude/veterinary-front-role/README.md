# Veterinary front role Expert

Role Expert for **Veterinary front role (not the vet)**. Appointment lists, records routing, reminders, boarding notes, estimates from their price file — not clinical care.

- Start: `QUICK-START.md`
- Role: `MyRole.txt`
- Method: `docs/role/work-item-method.md`
- Instructions: `CLAUDE.md`
- Memory: shared (`facts/facts-shared.md`, `facts/rules-shared.md`) then operations (`facts/facts-operations.md`, `facts/rules-operations.md`)
- Jobs: `.claude/workflows/` (registry: `workflow-registry.json`)
- Tools: `docs/tools/`

Each clinic date, patient pack, records request, estimate, or boarding drop-off is a Work Item under `work-items/<id>/` with `in/`, `work/`, `out/`, and `evidence/`. Journals live under `journals/`.
