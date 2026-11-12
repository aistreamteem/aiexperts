# How memory loading works

1. Read `facts/MEMORY-INDEX.md`.
2. Read `Workflow type` from the work-item journal.
3. Always load the shared pair: `facts-shared.md` and `rules-shared.md`.
4. Load the matching workflow pair:
   - `program-delivery` → `facts-program-delivery.md` and `rules-program-delivery.md`
   - `program-escalation` → `facts-program-escalation.md` and `rules-program-escalation.md`
5. Also load `work-items/<id>/facts/facts.md` and `rules.md` with no workflow filter.
6. Drop an expert-role entry whose `Workflows` list does not include the current workflow or `all`. Entries marked `all` belong in the shared pair.
7. Follow every loaded rule. Use facts as context.
8. Log the counts in the journal.

If the workflow is missing, default to `program-delivery`.

People-sensitive notes are not expert-role memory unless the operator explicitly said to store them.

The action hook reads `facts/trigger-index.json` and can surface a rule during any workflow when its trigger matches.
