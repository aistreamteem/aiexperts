---
name: remember
description: >-
  Store a durable fact or rule when the operator says remember, save this, or
  note this. Operations memory or the active Work Item facts folder.
---

# Remember

Files **facts** (what is true here) and **rules** (when / never). No vector store. This landscaping-office role uses operations memory only.

## When

Operator says “remember this”, “note this down”, “save this”, “capture this”, or you detect a shop correction worth saving.

## Do

1. Choose **kind**: `fact` (observation / how this shop files) or `rule` (must / never). Tools they use belong as facts pointing at `docs/tools/` (or a new tool stub they asked for).
2. If they did not say scope, ask: Work Item (this job only) vs Expert Role (every pack).
3. Cross-check `facts/facts-operations.md`, `facts/rules-operations.md`, and `work-items/<id>/facts/` if a Work Item is active. If similar, ask update vs new vs skip. If it contradicts, quote both and ask which is right — do not silently overwrite.
4. Expert Role default **Workflows:** `all`. Store in:
   - Facts: `facts/facts-operations.md`
   - Rules: `facts/rules-operations.md`
   - Work Item: `work-items/<id>/facts/facts.md` or `rules.md`
5. For rules, ask **Triggers** if a file write should surface it (`write:doc` for packs/markdown, `write:csv` for route/ticket sheets, or `none`). After a non-`none` trigger, run `python scripts/memory/build_trigger_index.py`.
6. If the entry is a new topic, add a pointer in `facts/MEMORY-INDEX.md`.
7. Confirm the path to the operator. Record a one-line note in the expert or Work Item journal.

**Not this skill:** decisions and Q&A → **journal-keeper**. Unverified wording → **operator-qa** first. Dropped packets / runbooks → **integrate-docs**.

Do not file into a many-file `docs/facts/` or `docs/rules/` tree as the live system. Use operations memory for this role.

## Examples (this role)

- Fact: “We call extras tickets, not work orders, on the mow route.”
- Rule: “Never invent a dump fee; ask if the price file has no line.”
- Fact: “Crew A roster export lives in the office Jobber CSV.”
