---
name: remember
description: >-
  Store a durable fact, rule, or tool pointer when the operator says remember,
  save this, or note this. Routes Expert Role captures into operations memory
  and Work Item captures into work-items/<id>/facts/.
---

# Remember

Captures facts and rules for this physical-therapy front role. Facts are observations/data (informative). Rules are constraints/procedures (prescriptive). Tools are how they use an app, file, or export.

## When to use

- Operator says "remember this", "note this down", "save this", "capture this", or similar
- Operator specifies scope inline ("remember this as a work-item fact")
- Agent proactively detects a reusable clinic pattern and the operator approves capture

## Memory locations

**Expert Role (this role):**
- Facts → `facts/facts-operations.md`
- Rules → `facts/rules-operations.md`
- Add a pointer in `facts/MEMORY-INDEX.md` when the capture introduces a new topic
- After a rule whose `Triggers:` is not `none`, run `python scripts/memory/build_trigger_index.py`

**Work Item:**
- `work-items/<id>/facts/facts.md`
- `work-items/<id>/facts/rules.md`

**Tools:**
- Pointer or new file under `docs/tools/` and a row in `docs/tools/INDEX.md`

Live Expert Role memory is the operations pair plus `docs/tools/`. Do not recreate a multi-file facts tree.

## Instructions

1. Choose **kind**: fact, rule, or tool.
2. Choose **scope**: Work Item vs Expert Role. Default Expert Role for clinic-wide procedure; Work Item for one date/pack.
3. Cross-check existing operations files and the active Work Item facts/rules. If similar, ask whether to update, add new, or skip.
4. If kind/scope was not specified, ask.
5. For Expert Role rules, ask for **Triggers** (comma-separate; `none` if background/judgment). Useful tokens for this role: `write:doc`, `write:csv`, `none`. Do not use SQL/PR tokens unless this clinic actually needs them.
6. Append a dated entry. Keep their wording. Label starter guesses.
7. Tell the operator the path. If the new statement contradicts an existing entry, quote both and ask which is right — do not silently replace.

**Not this skill:** decisions and Q&A → **journal-keeper**. Uncertain notes → **operator-qa** first.

### Entry shape (Expert Role)

```markdown
### YYYY-MM-DD: Short title
**Scope:** expert-role
**Workflows:** all
**Triggers:** none
**Captured:** YYYY-MM-DD
**Source:** operator
**Status:** active

**Starter / guess until they confirm this clinic.**

(Content.)
```

Omit `Triggers:` on facts. Work Item entries omit `Workflows:` (they inherit the job).
