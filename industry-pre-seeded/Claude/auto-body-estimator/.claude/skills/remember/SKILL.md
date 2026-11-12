---
name: remember
description: >-
  Store a durable fact, rule, or tool pointer when the operator says remember,
  save this, or note this. Expert Role memory is the shared pair; Work Item
  memory lives under work-items/<id>/facts/.
disable-model-invocation: false
---

# Remember

Files **facts, rules, or tools**. No vector store. Shared memory is how this role finds it later.

## When

Operator has something that must survive this chat (a correction, a shop rule, a file location).

## Do

1. Choose **kind**: `fact` (what is true here), `rule` (when / never), `tool` (how they use an app, file, or URL).
2. Choose **scope**:
   - **Work Item-level** — true only for this assignment / RO / claim → `work-items/<id>/facts/facts.md` or `.../rules.md`
   - **Expert Role-level** — true for this role going forward → `facts/facts-shared.md` or `facts/rules-shared.md`
3. If **tool**: append or create under `docs/tools/` and add a row to `docs/tools/INDEX.md`.
4. Infer a short **topic**. If the same topic already exists in the destination file, append to that entry. Otherwise add a new dated heading.
5. Append (Expert Role example):

```markdown
### YYYY-MM-DD: Short label
**Scope:** expert-role
**Workflows:** all
**Triggers:** none
**Captured:** YYYY-MM-DD
**Source:** operator
**Status:** active

(Content. Keep their wording. Preserve links.)

---
```

`Workflows: all` goes in the shared pair (`facts-shared.md` / `rules-shared.md`). Work Item entries omit **Workflows:** (they inherit this Work Item’s job). Trigger vocabulary: `write:doc`, `write:csv`, `write:estimate`, `write:photo-index`, `write:supplement`, `write:sql`, `sql:generate`, `pr:open`, `git:push`, `git:commit`, or `none`. Do not use `config:change`.

6. If a new Expert Role topic appears, add a pointer line to `facts/MEMORY-INDEX.md`.
7. If this contradicts an existing entry, show both and ask which is right. Do not silently overwrite.
8. Tell the operator the path. Confirm capture, then continue the prior task.

**Not this skill:** decisions and Q&A → **journal-keeper**. Batch docs → **integrate-docs**. Promoting Work Item knowledge → **promote-facts-rules**.
