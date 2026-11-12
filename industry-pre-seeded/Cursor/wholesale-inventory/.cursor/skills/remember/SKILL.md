---
name: remember
description: >-
  Store a durable fact or rule in shared or operations memory, or the Work Item
  facts folder, when the operator says remember, save this, or note this.
---

# Remember

Files **facts** (what is true here) and **rules** (when / never). No vector store. Inventory memory lives in shared + operations pairs plus optional Work Item files.

## When

Operator says remember / save this / note this, or a correction should survive this chat.

## Memory locations

- Shared facts (`Workflows: all`): `facts/facts-shared.md`
- Shared rules (`Workflows: all`): `facts/rules-shared.md`
- Operations facts (registered jobs): `facts/facts-operations.md`
- Operations rules (registered jobs): `facts/rules-operations.md`
- Work Item facts: `work-items/<id>/facts/facts.md`
- Work Item rules: `work-items/<id>/facts/rules.md`
- New topic pointer: `facts/MEMORY-INDEX.md`
- Tools (how they use a count sheet, PO PDF, scanner export): append or add under `docs/tools/` and `docs/tools/INDEX.md`

Do not write live memory under `docs/`. Route `Workflows: all` to the shared pair; job-specific Expert Role captures to the operations pair.

## Do

1. **Kind:** fact (observation) vs rule (must / never).
2. **Scope:** this Work Item only vs Expert Role (all future jobs). Inline phrases such as “remember this as an expert rule” skip the question.
3. Cross-check existing shared, operations, and Work Item files. If similar, ask: update / new / skip. If it **conflicts**, ask which is right before changing memory.
4. Expert Role entries use `**Workflows:**` = the registered job (`receiving-match`, `cycle-count`, …) or `all`. Default `all` unless the note is job-specific. Route `all` → shared pair; a named job → operations pair.
5. Rules also get `**Triggers:**` — inventory action tokens, comma-separated, or `none`:
   - `write:csv` — about to write a receiving, count, pick, reorder, or other CSV
   - `write:pack` — about to write an `out/` pack
   - `write:doc` — about to write markdown notes
   - `none` — judgment only (ask, refuse, do not invent)
6. Append:

```markdown
### YYYY-MM-DD: Short label
**Scope:** work-item | expert-role
**Workflows:** all | receiving-match | cycle-count | …
**Triggers:** write:csv | write:pack | write:doc | none
**Captured:** YYYY-MM-DD
**Source:** operator
**Status:** active

Content or **Rule:** statement
```

7. Confirm the path and one-line summary, then return to the prior work. Remember is not a work-map step.
8. Never store passwords, bank logins, or card numbers.
9. After a rule whose trigger is not `none`, regenerate with `py -3 scripts/memory/build_trigger_index.py`.
