---
name: remember
description: >-
  Store a durable fact or rule when the operator says remember, save this,
  note this, or when a correction should survive this chat. Files into
  operations memory or the active Work Item facts folder.
---

# Remember

Files **facts** and **rules** for this HOA / association admin role. No vector store. Operations memory is how we find it later.

## When

Operator has something that must survive this chat, or you detected a reusable shop pattern and they approved capture.

## Do

1. Choose **kind**: `fact` (what is true here) or `rule` (when / never). Tools they already use can be noted as facts pointing at `docs/tools/`.
2. Choose **scope**:
   - Work Item → `work-items/<id>/facts/facts.md` or `.../rules.md`
   - Expert Role → `facts/facts-operations.md` or `facts/rules-operations.md`
3. If the operator did not specify kind/scope, ask. Inline phrases such as "remember this as an expert rule" skip the ask.
4. Cross-reference existing operations memory and the active Work Item facts/rules. If a match exists, ask whether to update, add, or skip.
5. Append a dated `### YYYY-MM-DD: Title` entry with **Scope**, **Workflows:** `all` (or the current registered workflow id), **Captured**, **Source**, and **Status:** `active`. Rules also get **Triggers:** (`write:doc`, `write:csv`, or `none`) and a **Rule:** sentence.
6. If the capture introduces a new topic, add a pointer under the operations section of `facts/MEMORY-INDEX.md`.
7. After appending a rule whose Triggers field is not `none`, run `python scripts/memory/build_trigger_index.py`.
8. Tell the operator the path. If this contradicts an existing entry, ask which is right; do not silently overwrite.

**Not this skill:** decisions and Q&A → **journal-keeper**. Operator docs dumps → **integrate-docs**. End-of-pack elevation → **promote-facts-rules**.

### Examples for this role

- Fact: "This community's architectural form requires a neighbor signature on page 2."
- Rule: "Never list two associations on the same aging CSV unless each row names the community."
- Work Item fact: "June 2026 board packet is missing the May approved minutes PDF."
