---
name: remember
description: >-
  Store a durable fact, rule, or tool pointer when the operator says
  remember, save this, note this, or when a correction must survive this chat.
---

# Remember

Files **facts, rules, or tools**. No vector store. Operations memory is how we find it later.

## When

Operator has something that must survive this chat (including a correction to how this catering office files counts, pack-outs, leftover forms, or fees).

## Do

1. Choose **kind**: `fact` (what is true here), `rule` (when / never), `tool` (how they use an app, file, or URL).
2. Choose **scope**: Work Item-level (`work-items/<id>/facts/facts.md` or `.../rules.md`) vs Expert Role-level (`facts/facts-operations.md` or `facts/rules-operations.md`). Tool pointers go in `docs/tools/` plus `docs/tools/INDEX.md`.
3. Infer a short **topic**. If a similar operations entry exists, append rather than invent a parallel file tree.
4. Append a dated entry. Preserve their wording.

Expert Role fact:

```markdown
### YYYY-MM-DD: Short title
**Scope:** expert-role
**Workflows:** all
**Captured:** YYYY-MM-DD
**Source:** operator
**Status:** active

(Content. Keep their wording. Preserve links.)
```

Expert Role rule: same header plus `**Triggers:**` (`write:doc`, `write:csv`, `git:commit`, `git:push`, `pr:open`, or `none`) and a `**Rule:**` line. Do not tag rules with a retired config-change token.

5. If this is a new browse topic, add a pointer under the operations section of `facts/MEMORY-INDEX.md`.
6. If a new rule’s Triggers field is not `none`, regenerate with `python scripts/memory/build_trigger_index.py`.
7. Tell the operator the path. If this contradicts an existing entry, quote both and **ask** which is right. Do not silently overwrite.

**Not this skill:** decisions and Q&A → **journal-keeper**. Batch docs → **integrate-docs**. Promotion off a finished Work Item → **promote-facts-rules**.
