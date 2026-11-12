---
name: remember
description: >-
  Store a durable fact, rule, or tool pointer when the operator says
  remember, save this, or note this. Operations memory is facts-operations
  / rules-operations (or the active Work Item facts files).
---

# Remember

Files **facts, rules, or tool notes** for this equipment-rental role. No vector store. `facts/MEMORY-INDEX.md` is how we find it later.

## When

Operator has something that must survive this chat (a yard rule, a column name, a rate-file location, a “we never…”).

## Do

1. Choose **kind**: `fact` (what is true here), `rule` (when / never), `tool` (how they use an app, file, or URL).
2. Infer a short **topic**.
3. Choose **scope**:
   - **Expert Role** (applies to all jobs) → `facts/facts-operations.md` or `facts/rules-operations.md`. Tool how-tos go under `docs/tools/` and a pointer in operations facts if needed.
   - **Work Item** (this contract/day/pack only) → `work-items/<id>/facts/facts.md` or `work-items/<id>/facts/rules.md`.
4. If the topic already exists, append. If new, add an entry and, for Expert Role topics, a pointer in `facts/MEMORY-INDEX.md` when it is a new heading worth finding later.
5. If unsure whether it is a fact or a rule, or whether the wording is right, use **operator-qa** before saving.
6. If the new statement conflicts with an existing entry, show both and ask which is right. Do not silently overwrite.
7. Append:

```markdown
### YYYY-MM-DD: Short label
**Scope:** expert-role | work-item
**Workflows:** all | <registry job id>
**Triggers:** write:doc | write:csv | none   # rules only; facts omit Triggers
**Captured:** YYYY-MM-DD
**Source:** operator
**Status:** active

(Content. Keep their wording. Preserve links.)
```

8. Tell the operator the path. Then return to the prior work.

**Not this skill:** decisions and Q&A → **journal-keeper**. Full job steps → the registered workflow file (edit with operator approval).
