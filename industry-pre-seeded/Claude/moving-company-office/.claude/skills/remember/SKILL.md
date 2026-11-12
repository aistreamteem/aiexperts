---
name: remember
description: >-
  Store a durable fact or rule when the operator says remember, save this,
  note this, or when a shop correction should survive this chat. Writes
  shared/operations memory or Work Item memory — not the old docs/facts INDEX tree.
---

# Remember

Captures facts and rules when the operator says "remember this", "note this down", "save this", or similar. Facts are observations/data (informative); rules are constraints/procedures (prescriptive).

## When

- Operator says "remember this", "note this down", "save this", "capture this"
- Operator specifies scope inline: "remember this as a work-item fact" / "expert rule"
- Agent proactively detects a reusable shop pattern

> **Memory model:** Expert Role memory for this role is **shared** (`Workflows: all`) plus **operations** (job-scoped). Work Item captures stay in `work-items/<id>/facts/facts.md` and `.../rules.md`. Do not create `docs/facts/*.md` as the live system. Tool how-tos stay under `docs/tools/`.

## Do

1. **Inline scope/type** if they said "as a work-item fact" / "expert rule" / similar. Otherwise ask.
2. **Cross-reference** `facts/facts-shared.md`, `facts/rules-shared.md`, `facts/facts-operations.md`, `facts/rules-operations.md`, and the active Work Item facts/rules. If a match exists, ask whether to update, add new, or skip.
3. **Classify**
   - **Fact:** how *this* shop files (rate book location, calendar columns, who owns claims)
   - **Rule:** must / never (never invent weight, rates only from their file, ask if binding type missing)
   - **Work Item:** this move only (this estimate number, this ticket disagreement)
   - **Expert Role:** reusable across moves
4. **Workflows (Expert Role only):** default `all`, or the current job id (`estimate-from-rate-file`, `crew-day`, …). Do not file under `developer` or `production-incident`.
5. **Triggers (rules only):** what the agent is about to do when this rule matters:
   - `write:csv` — about to write a work CSV
   - `write:doc` — about to write a pack markdown
   - `write:estimate` — about to draft estimate lines
   - `none` — judgment / ask, no discrete file action
6. **Store**
   - Work Item fact → `work-items/<id>/facts/facts.md`
   - Work Item rule → `work-items/<id>/facts/rules.md`
   - Expert Role fact with `Workflows: all` → `facts/facts-shared.md`
   - Expert Role rule with `Workflows: all` → `facts/rules-shared.md`
   - Expert Role fact job-scoped → `facts/facts-operations.md`
   - Expert Role rule job-scoped → `facts/rules-operations.md`
   - New topic pointer on `facts/MEMORY-INDEX.md` when needed
7. If a rule trigger is not `none`, run `python scripts/memory/build_trigger_index.py`.
8. Confirm the path. Record a one-line note in the matching journal (expert vs Work Item).

Entry header format: `### YYYY-MM-DD: Title` (see `facts/MEMORY-INDEX.md`).

**Not this skill:** decisions and Q&A → **journal-keeper**. Unverified notes → **operator-qa** first.

### Proactive detection

Watch for operator corrections ("stairs are on the extras sheet, not guessed"), shop constraints, and repeated filing patterns. Propose exact wording and scope. Capture only with approval; apply the correction immediately.

If two files disagree, quote both and ask which wins — do not tidy the disagreement into a new remembered "truth."
