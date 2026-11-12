---
name: remember
description: >-
  Store a durable fact or rule in operations memory or the Work Item facts
  folder when the operator says remember, save this, or note this.
---

# Remember

Files **facts** (what is true here) and **rules** (when / never). No vector store. Pest-office memory lives in the operations pair plus optional Work Item files.

## When

Operator says remember / save this / note this, or a correction should survive this chat.

## Memory locations

- Expert Role facts: `facts/facts-operations.md`
- Expert Role rules: `facts/rules-operations.md`
- Work Item facts: `work-items/<id>/facts/facts.md`
- Work Item rules: `work-items/<id>/facts/rules.md`
- New topic pointer: `facts/MEMORY-INDEX.md`
- Tools (how they use a route CSV, chemical log, bait-map PDF): append or add under `docs/tools/` and `docs/tools/INDEX.md`

Do not write live memory to `docs/facts/*.md` or `docs/rules/*.md`. Do not route to `facts-developer.md` or incident files.

## Do

1. **Kind:** fact (observation) vs rule (must / never).
2. **Scope:** this Work Item only vs Expert Role (all future packs). Inline phrases such as “remember this as an expert rule” skip the question.
3. Cross-check existing operations and Work Item files. If similar, ask: update / new / skip. If it **conflicts**, ask which is right before changing memory.
4. Expert Role entries use `**Workflows:**` = the registered job (`route-day`, `chemical-log-completeness`, `all`, …). Default `all` unless the note is job-specific.
5. Rules also get `**Triggers:**` — pest-office action tokens, comma-separated, or `none`:
   - `write:csv` — about to write a route, ticket, skip, log, or index CSV
   - `write:pack` — about to write an `out/` pack
   - `write:doc` — about to write markdown notes
   - `none` — judgment only (ask, refuse, do not invent)
6. Append:

```markdown
### YYYY-MM-DD: Short label
**Scope:** work-item | expert-role
**Workflows:** all | route-day | chemical-log-completeness | …
**Triggers:** write:csv | write:pack | write:doc | none
**Captured:** YYYY-MM-DD
**Source:** operator
**Status:** active

(Content. Keep their wording.)
```

7. If you stored a rule whose trigger is not `none`, run `python scripts/memory/build_trigger_index.py`.
8. Confirm the path. Journal that it was saved.

**Examples:** “We key accounts as site, not billing customer” → expert-role fact. “Never invent an EPA number” → expert-role rule, trigger `write:csv`. “Tuesday’s ticket 118 is a courtesy callback, not a new sale” → Work Item fact.

**Not this skill:** decisions and Q&A → **journal-keeper**. Large dropped docs → **integrate-docs**. Unverified wording → **operator-qa** first.
