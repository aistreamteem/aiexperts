---
name: remember
description: >-
  Store a durable fact or rule in shared memory or the Work Item facts
  folder when the operator says remember, save this, or note this.
---

# Remember

Files **facts** (what is true here) and **rules** (when / never). No vector store. Processor memory lives in the shared pair plus optional Work Item files.

## When

Operator says remember / save this / note this, or a correction should survive this chat.

## Memory locations

- Expert Role facts: `facts/facts-shared.md`
- Expert Role rules: `facts/rules-shared.md`
- Work Item facts: `work-items/<id>/facts/facts.md`
- Work Item rules: `work-items/<id>/facts/rules.md`
- New topic pointer: `facts/MEMORY-INDEX.md`
- Tools (how they use an LOS export, a conditions sheet, a PDF folder): append or add under `docs/tools/` and `docs/tools/INDEX.md`

Do not write live memory to a multi-file `docs/facts/` or `docs/rules/` tree. Route Expert Role captures to the shared pair only.

## Do

1. **Kind:** fact (observation) vs rule (must / never).
2. **Scope:** this Work Item only vs Expert Role (all future packs). Inline phrases such as “remember this as an expert rule” skip the question.
3. Cross-check existing shared and Work Item files. If similar, ask: update / new / skip. If it **conflicts**, ask which is right before changing memory.
4. Expert Role entries use `**Workflows:**` = the registered job (`conditions-checklist`, `missing-docs`, `all`, …). Default `all` unless the note is job-specific.
5. Rules also get `**Triggers:**` — processor action tokens, comma-separated, or `none`:
   - `write:csv` — about to write a conditions, index, or date CSV
   - `write:pack` — about to write an `out/` checklist or missing-docs pack
   - `write:doc` — about to write markdown notes
   - `none` — judgment only (ask, refuse, do not invent)
6. Append:

```markdown
### YYYY-MM-DD: Short label
**Scope:** work-item | expert-role
**Workflows:** all | conditions-checklist | missing-docs | …
**Triggers:** write:csv | write:pack | write:doc | none
**Captured:** YYYY-MM-DD
**Source:** operator
**Status:** active

(Content. Keep their wording.)

---
```

7. If you stored a rule whose trigger is not `none`, run `python scripts/memory/build_trigger_index.py`.
8. Confirm the path. Journal that it was saved.

**Examples:** “This shop exports PTD as PriorToDocs” → expert-role fact. “Never declare CTC from a green checklist” → expert-role rule, trigger `write:pack`. “Loan 4412 uses a split gift trail in in/gift/” → Work Item fact.

**Not this skill:** decisions and Q&A → **journal-keeper**. Large dropped docs → **integrate-docs**. Unverified wording → **operator-qa** first.
