---
name: remember
description: >-
  Store a durable fact, rule, or tool pointer when the operator says
  remember, save this, or note this.
---

# Remember

Files **facts, rules, or tools** for this clinic front role. No vector store. Operations memory plus MEMORY-INDEX is how we find it later.

## When

Operator has something that must survive this chat. Also after a confirmed correction that should become clinic procedure.

## Do

1. Choose **kind**: `fact` (what is true here), `rule` (when / never), `tool` (how they use an app, file, or folder).
2. Choose **scope**: Work Item-level (this appointment/date/pack only) or Expert Role-level (all future Work Items).
3. Ask if scope or kind is unclear. Do not invent clinic procedure; store their wording.

4. **Expert Role fact** → if `Workflows: all`, append to `facts/facts-shared.md`; otherwise append to `facts/facts-operations.md`.
   **Expert Role rule** → if `Workflows: all`, append to `facts/rules-shared.md`; otherwise `facts/rules-operations.md`. Include `**Triggers:**` (`none` unless they name a tool-action such as `write:csv`, `write:pack`, or `write:doc`).
   **Work Item fact/rule** → `work-items/<id>/facts/facts.md` or `.../rules.md`.
   **Tool** → `docs/tools/<topic>.md` and a row in `docs/tools/INDEX.md` (or `docs/tools/captured.md` if unsure).

5. Entry shape for operations memory:

```markdown
### YYYY-MM-DD: Short title
**Scope:** expert-role
**Workflows:** all
**Triggers:** none
**Captured:** YYYY-MM-DD
**Source:** operator
**Status:** active

(Content. Keep their wording. Preserve links.)
```

6. If the new topic is not listed in `facts/MEMORY-INDEX.md`, add a pointer under Operations. After a rule whose Triggers is not `none`, run `python scripts/memory/build_trigger_index.py`.

7. Tell the operator the path. If this contradicts an existing entry, quote both and ask which is right before replacing.

**Not this skill:** decisions and Q&A → **journal-keeper** / **operator-qa**. Recurring jobs → a workflow file under `.claude/workflows/` plus the registry (operator must confirm).
