---
name: remember
description: >-
  Store a durable fact, rule, or tool pointer when the operator says remember,
  save this, or note this. Files into operations memory or the active Work Item.
---

# Remember

Files **facts, rules, or tools** so they survive this chat. No vector store.

## When

Operator says remember / save this / note this, or a confirmed correction must persist.

## Do

1. Choose **kind**: `fact` (what is true here), `rule` (when / never), `tool` (how they use a sheet, PDF folder, or app).
2. Choose **scope**:
   - Expert Role (applies to every kitchen job) → `facts/facts-operations.md` or `facts/rules-operations.md`
   - This Work Item only → `work-items/<id>/facts/facts.md` or `.../rules.md`
   - Tool → `docs/tools/<topic>.md` and a row in `docs/tools/INDEX.md`
3. Infer a short **topic** (lowercase). Ask if scope is unclear.
4. If this contradicts an existing operations entry, quote both and ask which is live. Do not silently overwrite.
5. Append using the operations entry format (see `facts/MEMORY-INDEX.md`):

```markdown
### YYYY-MM-DD: Short label
**Scope:** expert-role | work-item
**Workflows:** all | prep | count-walk-in | order-guide | receiving | invoice-match | eighty-six | par-review | waste-week | catering-pull | allergen-quote
**Triggers:** none | write:sheet | write:pack | file:intake
**Captured:** YYYY-MM-DD
**Source:** operator | file path
**Status:** active

(Content. Keep their wording. Preserve links.)
```

For a **rule**, include `**Rule:**` as the first line of the body. Default `**Triggers:**` to `none` unless the rule should fire on writing a sheet/pack or taking in a file. Do not tag rules with a retired config-change token.

6. After appending a rule whose Triggers is not `none`, run `python scripts/memory/build_trigger_index.py`.
7. Tell the operator the path. Confirm what was saved.

**Not this skill:** decisions and Q&A → **journal-keeper**. Dropped handbooks or multi-page notes → **integrate-docs**.

Live memory is the operations pair plus MEMORY-INDEX. Do not recreate a multi-file facts tree.
