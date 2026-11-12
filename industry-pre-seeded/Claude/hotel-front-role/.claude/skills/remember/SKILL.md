---
name: remember
description: >-
  Store a durable fact or rule in operations memory or Work Item facts when
  the operator says remember, save this, or note this.
---

# Remember

Files **facts** (what is true here) or **rules** (when / never). No vector store. Operations memory is how we find it later.

## When

Operator has something that must survive this chat. Also after a correction they approved as durable.

## Do

1. Choose **kind**: `fact` (what is true here) or `rule` (when / never). Tool pointers go in `docs/tools/` (update `docs/tools/INDEX.md` if new).
2. Choose **scope**:
   - **Expert Role** → `facts/facts-operations.md` or `facts/rules-operations.md`
   - **Work Item** → `work-items/<id>/facts/facts.md` or `work-items/<id>/facts/rules.md`
3. Infer a short **topic**. If a similar entry exists, append or ask which wording wins (do not invent a merge).
4. Append a dated entry:

```markdown
### YYYY-MM-DD: Short label

**Scope:** expert-role | work-item
**Workflows:** all
**Triggers:** none
**Captured:** YYYY-MM-DD
**Source:** operator
**Status:** active

(Content. Keep their wording. Preserve links.)
```

Rules also need **Rule:** / **Why:** when the operator gave a constraint. For a rule, ask which action trigger to set (`write:doc`, `write:csv`, `none`). After a non-`none` trigger, run `py -3 scripts/memory/build_trigger_index.py`.

5. If the entry introduces a new browsing topic, add a pointer on `facts/MEMORY-INDEX.md`.
6. Tell the operator the path. If this contradicts an existing entry, show both and ask which is right.

**Not this skill:** decisions and Q&A → **journal-keeper** / **operator-qa**. Batch docs → **integrate-docs**.
