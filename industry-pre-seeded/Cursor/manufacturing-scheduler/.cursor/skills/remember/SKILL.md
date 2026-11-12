---
name: remember
description: >-
  Store a durable fact, rule, or tool pointer when the operator says remember,
  save this, or note this. Expert Role memory goes in facts-shared /
  rules-shared (Workflows: all) or facts-operations / rules-operations;
  Work Item memory stays under work-items/<id>/facts/.
---

# Remember

File **facts, rules, or tools** so the next scheduler pack is closer to *this* shop. No vector store.

## When

Operator says "remember this", "note this down", "save this", "capture this", or similar. Also when you detect a reusable shop pattern and they approve capturing it.

## Do

1. Choose **kind**: `fact` (what is true here), `rule` (when / never), `tool` (how they use an app, file, or export).
2. Choose **scope**:
   - Work Item — true only for this pack / WO / board → `work-items/<id>/facts/facts.md` or `.../rules.md`
   - Expert Role, `Workflows: all` → `facts/facts-shared.md` or `facts/rules-shared.md`
   - Expert Role, one registered job → `facts/facts-operations.md` or `facts/rules-operations.md`
   - Tool pointer → `docs/tools/<topic>.md` and a row in `docs/tools/INDEX.md`
3. If the operator did not specify kind/scope, ask: fact vs rule, Work Item vs Expert Role, and shared vs job-specific.
4. Cross-check shared + operations memory and this Work Item’s facts/rules. If similar, ask update vs new vs skip.
5. Append an Expert Role entry:

```markdown
### YYYY-MM-DD: Short title
**Scope:** expert-role
**Workflows:** all
**Triggers:** none
**Captured:** YYYY-MM-DD
**Source:** operator
**Status:** active

(Content. Keep their wording.)
```

   For a rule, include `**Rule:**` and keep `**Triggers:** none` unless they named a real file-write action (`write:doc` or `write:csv`). Prefer `none` or `write:doc` on this role. Vocabulary for the action hook: `write:doc`, `write:csv` (no `config:change`).
6. Tell the operator the path. If the new statement contradicts an existing entry, quote both and ask which is right before writing.
7. After adding a rule whose Triggers is not `none`, run `py -3 scripts/memory/build_trigger_index.py`.
8. **journal-keeper** if this changes what the current pack will do.

**Not this skill:** decisions and Q&A → **journal-keeper** / **operator-qa**. Batch docs → **integrate-docs**. Promotion at pack end → **promote-facts-rules**.
