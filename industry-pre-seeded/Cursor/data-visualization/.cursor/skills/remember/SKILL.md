---
name: remember
description: >-
  Store a durable fact or rule in operations memory or Work Item memory when
  the operator says remember, save this, or note this.
---

# Remember

Files **facts** or **rules** so the next chart pack is closer to this shop. No vector store. `facts/MEMORY-INDEX.md` is how we find it later. Tool pointers belong under `docs/tools/` with a short fact that names the tool file.

## When

Operator has something that must survive this chat (export names, week-start, color override, compare order, a never).

## Do

1. Choose **kind**: `fact` (what is true here) or `rule` (when / never). If they described how they use an app or file, write a `docs/tools/<topic>.md` stub and a fact that points at it.
2. Choose **scope**:
   - **Work Item-level** → `work-items/<id>/facts/facts.md` or `work-items/<id>/facts/rules.md`
   - **Expert Role-level, Workflows: all** → `facts/facts-shared.md` or `facts/rules-shared.md`
   - **Expert Role-level, chart-job specific** → `facts/facts-operations.md` or `facts/rules-operations.md`
3. Infer a short **topic**. If the topic is new at Expert Role level, add a pointer in `facts/MEMORY-INDEX.md`.
4. If a new statement conflicts with an existing fact or rule, show both and ask which is right. Do not silently overwrite.
5. Append using the entry format in `facts/MEMORY-INDEX.md` (`### YYYY-MM-DD: Title`). Preserve their wording. Label guesses as guesses.
6. For a **rule**, set `**Triggers:**` if an action should surface it (`write:python`, `write:csv`, `write:chart`, `write:doc`, or `none`). After adding a non-`none` trigger, run `python scripts/memory/build_trigger_index.py`.
7. Tell the operator the path.

**Not this skill:** decisions and Q&A → **journal-keeper**. Unverified notes → **operator-qa** first. Batch docs → **integrate-docs**.
