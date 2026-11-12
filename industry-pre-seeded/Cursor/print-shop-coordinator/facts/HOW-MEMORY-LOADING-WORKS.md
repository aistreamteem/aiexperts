# How memory loading works

Short mechanism note for this print-shop coordinator expert. Starter entries live in the shared pair until the operator corrects them.

## What loads

1. `facts/MEMORY-INDEX.md` — navigation and entry format.
2. `facts/facts-shared.md` and `facts/rules-shared.md` — Expert Role memory for every registered job.
3. Active Work Item `work-items/<id>/facts/facts.md` and `rules.md` when present.
4. Filter Expert Role entries by `**Workflows:**` (`all` or the current registry id such as `job-board`).

## When it loads

- **continue** step 0f and the start of role skills that touch shop knowledge.
- **remember** / **promote-facts-rules** / **integrate-docs** when capturing or promoting.
- PreToolUse hook `.cursor/hooks/inject_rules_on_action.py` surfaces rules tagged with a live trigger token from `facts/trigger-index.json`.

## Pointers

- Active Work Item: `.cursor/active-context.txt` (`work-item:<id>`). Legacy `.cursor/active-work-item.txt` is read-only fallback.
- Journals: `journals/expert/progress.md` and `journals/work-items/<id>/`.
- Regenerate triggers after retagging a rule: `python scripts/memory/build_trigger_index.py`.

## What this file is not

It does not report line counts, timings, or folders this scaffold does not have (`incident-sessions/`, developer memory pairs, or a second top-level expert facts file named like the old unsplit memory).
