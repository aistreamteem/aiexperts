---
name: remember
description: >-
  Store a durable fact, rule, or tool pointer when the operator says remember,
  save this, note this, or when a shop correction must survive this chat.
---

# Remember

Files **facts, rules, or tools** for this church-office role. No vector store. Shared memory plus MEMORY-INDEX is how we find it later.

## When

Operator has something that must survive this chat: a shop correction, a live process-file location, a fund-chart list, a “never” constraint.

## Do

1. Choose **kind**: `fact` (what is true here), `rule` (when / never), `tool` (how they use an app, file, or URL).
2. Infer a short **topic** (lowercase). Ask if kind or topic is unclear.
3. Choose **scope**:
   - **Work Item-level** — true only for this Sunday, batch, roster, or meeting → `work-items/<id>/facts/facts.md` or `.../rules.md`
   - **Expert Role-level** — true for this shop across jobs → `facts/facts-shared.md` or `facts/rules-shared.md`
   - **Tool** — `docs/tools/<topic>.md` and a row in `docs/tools/INDEX.md`
4. If a similar entry exists, show both and ask whether to append, replace, or keep separate. Do not silently overwrite.
5. Append a dated entry. Preserve their wording. Expert Role format:

```markdown
### YYYY-MM-DD: Short title
**Scope:** expert-role
**Workflows:** all | giving-batch-from-export | week-calendar | (registry id or comma-separated)
**Triggers:** none | write:doc | write:csv
**Captured:** YYYY-MM-DD
**Source:** operator
**Status:** active

(Content. Keep their wording. Preserve links.)
```

Work Item entries omit **Workflows:** (they inherit the Work Item). `Workflows: all` goes in the **shared** pair.

6. After appending a **rule** whose Triggers is not `none`, run `python scripts/memory/build_trigger_index.py`.
7. Tell the operator the path. If this contradicts an existing entry, ask which is right before writing.

**Not this skill:** decisions and Q&A → **journal-keeper**. Batch handbooks → **integrate-docs**. Elevating a Work Item note to shop-wide → **promote-facts-rules**.

Do not invent coding-standard or incident-response buckets. This role’s Expert Role memory is the shared pair only.
