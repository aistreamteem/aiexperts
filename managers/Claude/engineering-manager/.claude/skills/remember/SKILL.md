---
name: remember
description: "Use when the operator says remember this, or when a reusable management fact or rule appears. Classifies and stores it."
trigger: User says "remember this" or a new rule is detected
---

# Remember

## When to use

The operator says "remember this", "note this down", "save this", or you detect a repeated pattern and they agree to store it.

## Steps

1. If they did not already say, ask whether it is a **fact** (what is true) or a **rule** (what must be done), and whether it is **work-item** or **expert-role**.
2. Expert-role entries need `Workflows`: `team-delivery`, `team-escalation`, `all`, or a comma-separated list. Ask if it is unclear. Also ask for `Triggers` on a rule. Use `none` when no action should surface it. Starter triggers include: meeting:1on1, hiring:loop, status:update, escalation:open, decision:log, write:doc.
3. People-sensitive material (private conversations, performance, personal circumstances) is not stored in expert-role memory unless the operator explicitly says to store it. Offer to keep it on the work item instead.
4. Show the entry, then write it.
   - Work item: `work-items/<id>/facts/facts.md` or `rules.md`
   - Expert role with `Workflows: all`: `facts/facts-shared.md` or `facts/rules-shared.md`
   - Expert role for one workflow: `facts/facts-<workflow>.md` or `facts/rules-<workflow>.md`
5. Use the entry shape in `facts/MEMORY-INDEX.md` (`### YYYY-MM-DD: Title`). Check for a duplicate first.
6. Confirm what was stored and where. Mention regenerating the trigger index when a rule's triggers changed: `python scripts/memory/build_trigger_index.py`.
7. Record the capture on the matching layer: the expert journal, the work item journal, or the active node's note file. Facts and rules themselves stay in `facts/`.

## Proactive detection

During intake, charter, plan, execute, change-request, or escalation, if the operator states a constraint you would reuse, propose the fact or rule and its scope. Store it only after they agree.

## Verify before persist

When notes or proposed memory need operator confirmation before writing, open an `operator-qa` session, record the verification answers in that journal, close to `conclusions.md`, then store only the verified wording.
