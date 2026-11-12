---
name: remember
description: >-
  Store a durable fact or rule when the operator says remember, save this,
  or note this. Expert Role memory goes in operations files; Work Item
  memory goes under work-items/<id>/facts/.
---

# Remember

Files **facts** (what is true here) and **rules** (when / never). No vector store. Operations memory plus MEMORY-INDEX is how we find it later. Tool how-to still lives under `docs/tools/` — if they describe a shop tool, add or append there and mention the path.

## When

Operator has something that must survive this chat.

## Do

1. Choose **kind**: `fact` (what is true here) or `rule` (when / never). If they described how they use an app, file, or URL, treat it as a tool pointer under `docs/tools/` (and optionally a fact that names the tool).
2. Ask **scope** if unclear: Work Item-level vs Expert Role-level. Default Expert Role for shop-wide practice; Work Item for this site-night or pack only.
3. Infer a short **topic**.
4. Write:
   - `Workflows: all` Expert Role fact → `facts/facts-shared.md`
   - `Workflows: all` Expert Role rule → `facts/rules-shared.md`
   - Job-scoped Expert Role fact → `facts/facts-operations.md`
   - Job-scoped Expert Role rule → `facts/rules-operations.md`
   - Work Item fact → `work-items/<id>/facts/facts.md`
   - Work Item rule → `work-items/<id>/facts/rules.md`
   - Unsure → ask, or park a dated note at the end of the matching file labeled captured.
5. Use this shape:

```markdown
### YYYY-MM-DD: Short label
**Scope:** expert-role | work-item
**Workflows:** all | night-board | complaint-callback | … (Expert Role only)
**Triggers:** none | write:doc | write:sheet | write:csv | write:file (rules only)
**Captured:** YYYY-MM-DD
**Source:** (their words / file)
**Status:** active

(Content. Keep their wording. Preserve links.)
```

6. If the entry introduces a new topic, add a pointer in `facts/MEMORY-INDEX.md`. After adding a rule whose Triggers is not `none`, run `python scripts/memory/build_trigger_index.py`.
7. Tell the operator the path. If this contradicts an existing entry, quote both and ask which is right before saving.

**Not this skill:** decisions and Q&A → **journal-keeper**. Batch docs → **integrate-docs**.
