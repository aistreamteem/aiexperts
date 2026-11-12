---
name: remember
description: >-
  Store a durable fact, rule, or tool pointer when the operator says remember,
  save this, note this, or when a correction must survive this chat.
---

# Remember

Files **facts, rules, or tools** for this real-estate transaction-coordinator role. No vector store. Operations memory is how we find it later.

## When

Operator has something that must survive this chat (a shop form name, a filing pattern, a never-do, a tool they actually use).

## Do

1. Choose **kind**: `fact` (what is true here), `rule` (when / never), `tool` (how they use an app, file, or URL).
2. Choose **scope**:
   - **Work Item** — true only for this transaction file → `work-items/<id>/facts/facts.md` or `.../rules.md`
   - **Expert Role** — true for the role → `facts/facts-operations.md` or `facts/rules-operations.md`
3. Infer a short **topic**. Ask if scope or kind is unclear.
4. For Expert Role facts/rules, set `**Workflows:**` to `all` or the current role job id. For rules, set `**Triggers:**` (`write:doc`, `write:checklist`, `none`).
5. Append using the operations entry format (date header, Scope, Workflows, Captured, Source, Status). Preserve their wording.
6. For a **tool**, add or update `docs/tools/<topic>.md` and a row in `docs/tools/INDEX.md`. No passwords.
7. If this contradicts an existing entry, ask which is right. Do not silently overwrite.
8. Tell the operator the path. If a rule trigger is not `none`, regenerate with `python scripts/memory/build_trigger_index.py`.

**Not this skill:** decisions and Q&A → **journal-keeper**. Batch documentation dumps → **integrate-docs**.
