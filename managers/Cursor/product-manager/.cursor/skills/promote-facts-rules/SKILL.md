---
name: promote-facts-rules
description: "Use when a work item is done or the operator asks to promote facts and rules into expert-role memory."
trigger: Work item is done, or user asks to promote facts/rules
---

# Promote facts and rules

## Journal layer

Step notes and the next action go on the active node through journal-keeper, in `journals/work-items/<id>/nodes/`. Item-wide fields stay in `journals/work-items/<id>/progress.md`. Artifacts live under `work-items/<id>/`. Use AskQuestion for a fixed choice.

1. Read `work-items/<id>/facts/facts.md` and `rules.md`. List entries whose status is still active.
2. Ask, one group at a time, which entries to promote. Skip people-sensitive notes unless the operator explicitly says to promote them.
3. Generalize wording that only makes sense for this one work item.
4. Write promoted entries into the matching expert-role file: `facts/facts-shared.md` / `facts/rules-shared.md` when `Workflows` is `all`, otherwise `facts/facts-product-initiative.md` / `facts/rules-product-initiative.md` or the `product-escalation` pair. Include `Workflows` and, for rules, `Triggers` (starter set includes `write:doc`).
5. Mark the work-item copy `promoted-to-expert`.
6. Record the promotions in the journal.
7. If the work item used a cadence the registry does not name, ask whether to add a pipeline to MyRole.txt. Add it only after they agree, and add the workflow file and registry entry in that same turn.
8. Remind the operator that expert-role files changed, and regenerate the trigger index when a rule moved.
