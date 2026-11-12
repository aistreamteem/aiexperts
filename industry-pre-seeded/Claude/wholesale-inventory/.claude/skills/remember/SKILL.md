---
name: remember
description: >-
  Store a durable fact or rule in shared/operations memory or the Work Item facts
  folder when the operator says remember, save this, or note this.
---

# Remember

Files **facts** (what is true here) and **rules** (when / never). No vector store. Inventory memory lives in the shared and operations pairs plus optional Work Item files.

## When

Operator says remember / save this / note this, or a correction should survive this chat.

## Memory locations

- Shared facts (`Workflows: all`): `facts/facts-shared.md`
- Shared rules (`Workflows: all`): `facts/rules-shared.md`
- Operations facts: `facts/facts-operations.md`
- Operations rules: `facts/rules-operations.md`
- Work Item facts: `work-items/<id>/facts/facts.md`
- Work Item rules: `work-items/<id>/facts/rules.md`
- New topic pointer: `facts/MEMORY-INDEX.md`
- Tools (how they use a WMS export, CSV layout, folder): append or add under `docs/tools/` and `docs/tools/INDEX.md`

Do not write live memory to a multi-file `docs/facts/` or `docs/rules/` tree. Route `Workflows: all` Expert Role captures to the **shared** pair; job-scoped Expert Role captures to the **operations** pair.

## Do

1. **Kind:** fact (observation) vs rule (must / never).
2. **Scope:** this Work Item only vs Expert Role (all future packs). Inline phrases such as “remember this as an expert rule” skip the question.
3. Cross-check existing shared, operations, and Work Item files. If similar, ask: update / new / skip. If it **conflicts**, ask which is right before changing memory.
4. Expert Role entries use `**Workflows:**` = the registered job (`receiving-match`, `cycle-count`, `all`, …). Default `all` unless the note is job-specific. Route `all` → shared; a named job → operations.
5. Rules also get `**Triggers:**` — inventory action tokens, comma-separated, or `none`:
   - `write:csv` — about to write a count, match, pick, or reorder CSV
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

(Content. Keep their wording.)

---
```

7. If you stored a rule whose trigger is not `none`, run `python scripts/memory/build_trigger_index.py`.
8. Confirm the path. Journal that it was saved.

**Examples:** “Recount threshold is 2 units or 1%” → expert-role fact (`cycle-count` → operations). “Never invent on-hand qty” → expert-role rule (`all` → shared), trigger `none`. “This receipt’s slip used case UOM” → Work Item fact.

**Not this skill:** decisions and Q&A → **journal-keeper**. Large dropped docs → **integrate-docs**. Unverified wording → **operator-qa** first.
