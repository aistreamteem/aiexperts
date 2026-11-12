---
name: remember
description: >-
  Store a durable fact or rule when the operator says remember, save this,
  note this, or when a correction about how this center files should survive
  this chat.
---

# Remember

Files **facts** (what is true here) and **rules** (when / never) into operations memory or the active Work Item. Tools the shop uses are noted in `docs/tools/` (and may be pointed at from a fact). No vector store. `facts/MEMORY-INDEX.md` is how later sessions find it.

## When

Operator says "remember this", "note this down", "save this", "capture this", or similar. Also when the Expert proposes a new reusable pattern and the operator approves.

## Memory model

Expert Role memory for this role:

- `Workflows: all` → `facts/facts-shared.md` / `facts/rules-shared.md` (always loaded)
- Registered job id → `facts/facts-operations.md` / `facts/rules-operations.md`
- New topics → add a pointer in `facts/MEMORY-INDEX.md`

Work Item captures stay in:

- `work-items/<id>/facts/facts.md`
- `work-items/<id>/facts/rules.md`

Do not write a multi-file `docs/facts/` or `docs/rules/` tree as the live system. Do not invent software-build or incident-response memory files — those are not this role’s memory.

## Do

1. **Inline scope/type** if they said "as a work-item fact" / "as an expert rule". Otherwise ask.
2. **Type:** fact (observation/data: their export headers, room names, which calendar is live) vs rule (constraint: never release a child, never invent tuition, ask on pickup mismatch).
3. **Scope:**
   - Work Item: this date/room/child/packet only
   - Expert Role: how *this* center always files (after they confirmed it is not just a starter guess)
4. **Cross-check** shared + operations + the active Work Item facts/rules. If similar, ask update vs new vs skip.
5. **Workflows:** use `all` for cross-job notes (route to shared). Name a registered job id (`attendance-day`, `pickup-list-check`, …) when the note only applies there (route to operations).
6. **Triggers (rules only):** action tokens useful on this role, comma-separated, or `none`:
   - `write:doc` — writing a pack, list, or markdown
   - `write:csv` — writing a grid or export copy
   - `none` — background/judgment (most childcare-office rules)
   - Do not invent `config:change`, `write:sql`, `pr:open`, or `git:push` unless the operator insists
7. Append with heading `### YYYY-MM-DD: Title` (Scope, Workflows, Captured, Source, Status; rules also get Triggers, Rule, Why, How to apply).
8. After a rule whose Triggers is not `none`, run `python scripts/memory/build_trigger_index.py`.
9. Tell the operator the path. If it contradicts an existing entry, show both and ask which is right — do not silently overwrite.

**Not this skill:** decisions and Q&A → **journal-keeper** (and **operator-qa** to verify wording first when unsure).
