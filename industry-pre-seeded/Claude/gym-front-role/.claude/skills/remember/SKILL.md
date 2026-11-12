---
name: remember
description: >-
  Store a durable fact, rule, or tool pointer when the operator says remember,
  save this, note this, or when a club correction must survive this chat.
---

# Remember

Files **facts, rules, or tools** for this gym / fitness front role. No vector store.

## When

Operator has something that must survive this chat: a club vocabulary correction, a policy-file location, a column name on their export, a never-do.

## Do

1. Choose **kind**: `fact` (what is true here), `rule` (when / never), `tool` (how they use an app, file, or URL).
2. Choose **scope**:
   - **Work Item** — true only for this day/member/class/pack → `work-items/<id>/facts/facts.md` or `.../rules.md`
   - **Expert Role** — `Workflows: all` → `facts/facts-shared.md` / `facts/rules-shared.md`; job-scoped → `facts/facts-operations.md` / `facts/rules-operations.md`
   - **Tool** — `docs/tools/<topic>.md` and a row in `docs/tools/INDEX.md`
3. Infer a short **topic**. Ask if scope is unclear. Operator may say "remember this as a work-item fact" or "remember this as an expert rule".
4. For Expert Role entries, set `**Workflows:**` to `all` or the role job ids it applies to (`check-in-day`, `retail-close`, …). Default `all`.
5. For a **rule**, ask for `**Triggers:**` (comma-separated; `none` if judgment-only). Vocabulary: `write:doc`, `write:csv`, `write:pack`, `none`. Do not invent configuration-change or developer SQL/PR tokens.
6. Append using the operations entry format (date heading, Scope, Workflows, Captured, Source, Status). Keep their wording. Label starter guesses as starter.
7. If this contradicts an existing entry, **ask which is right** before overwriting. Do not silently replace.
8. Tell the operator the path. If a rule trigger is not `none`, regenerate `facts/trigger-index.json` with `python scripts/memory/build_trigger_index.py`.
9. **journal-keeper**: note the capture.

**Not this skill:** decisions and Q&A → **journal-keeper**. Large dropped packets → **integrate-docs**. Elevating Work Item memory after the pack is done → **promote-facts-rules**.
