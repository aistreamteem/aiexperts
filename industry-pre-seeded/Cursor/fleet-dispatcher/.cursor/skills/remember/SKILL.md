---
name: remember
description: >-
  Store a durable fact, rule, or tool pointer when the operator says remember,
  save this, or note this. Routes Expert Role entries into shared or operations
  memory and Work Item entries into work-items/<id>/facts/.
---

# Remember

Files **facts, rules, or tools** so they survive this chat. No vector store.

## When

Operator has something that must survive this chat (including a correction about how *this* fleet works).

## Do

1. Choose **kind**: `fact` (what is true here), `rule` (when / never), `tool` (how they use an app, file, or URL).
2. Infer a short **topic** (lowercase). Ask if unclear.
3. Choose **scope**:
   - **Work Item-level** → `work-items/<id>/facts/facts.md` or `.../rules.md` (or `docs/tools/` plus a pointer if it is a tool for this pack only)
   - **Expert Role-level, Workflows: all** → `facts/facts-shared.md` or `facts/rules-shared.md`
   - **Expert Role-level, a registered role job** → `facts/facts-operations.md` or `facts/rules-operations.md` (tools: `docs/tools/<topic>.md` and a row in `docs/tools/INDEX.md`)
4. If this contradicts an existing entry, show both and ask which is right. Do not silently overwrite.
5. Append using the entry shape in `facts/MEMORY-INDEX.md` (`### YYYY-MM-DD: Title`, scope, workflows, source, status). Keep their wording. Preserve links.
6. For a **rule**, ask for **Triggers:** if useful (`write:doc`, `write:csv`, `none`). Then regenerate `python scripts/memory/build_trigger_index.py` when the token is not `none`.
7. Tell the operator the path. Confirm, then resume the prior dispatch step.

**Not this skill:** decisions and Q&A → **journal-keeper** / **operator-qa**. Recurring jobs → a registered workflow file, not a parallel process skill.

Do not write to a multi-file `docs/facts/` tree as the live system. Use the shared/operations pairs (or this Work Item’s `facts/`) only.
