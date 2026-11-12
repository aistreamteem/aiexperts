---
name: remember
description: >-
  Store a durable fact, rule, or tool pointer when the operator says
  remember, save this, or note this.
disable-model-invocation: false
---

# Remember

Files **facts, rules, or tools** for this service-advisor role. No vector store. Shared + operations memory is how we find it later.

## When

Operator has something that must survive this chat. Also when a correction should change how the next RO pack is built.

## Do

1. Choose **kind**: `fact` (what is true here), `rule` (when / never), `tool` (how they use an app, file, or URL).
2. Choose **scope**:
   - **Expert Role, Workflows: all** → `facts/facts-shared.md` or `facts/rules-shared.md`
   - **Expert Role, this shop's RO jobs** → `facts/facts-operations.md` or `facts/rules-operations.md`
   - **Work Item** — this RO/pack only → `work-items/<id>/facts/facts.md` or `work-items/<id>/facts/rules.md`
3. Tools: add or update `docs/tools/<topic>.md` and a row in `docs/tools/INDEX.md`.
4. Infer a short **topic**. If the topic already exists, append. If new at Expert Role level, add a pointer in `facts/MEMORY-INDEX.md` when it is a new browse topic.
5. For rules that fire on a tool action, set `**Triggers:**` to a token the hook can produce (`write:doc`), otherwise `none`.
6. Append (Expert Role example):

```markdown
### YYYY-MM-DD: Short label
**Scope:** expert-role
**Workflows:** all
**Triggers:** none
**Captured:** YYYY-MM-DD
**Source:** operator
**Status:** active

(Content. Keep their wording. Preserve links.)
```

7. After appending a rule whose Triggers is not `none`, run `python scripts/memory/build_trigger_index.py`.
8. Tell the operator the path. If this contradicts an existing entry, ask which is right (**operator-qa** for a fixed choice), then save the winner.

**Not this skill:** decisions and Q&A → **journal-keeper**. Do not write live memory as many files under `docs/facts/` or `docs/rules/`.
