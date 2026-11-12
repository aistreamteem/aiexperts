# How memory loading works

**Answer:** This bakery / cafe production-office expert loads **shared** memory, then **operations** memory, then the active Work Item files. Default job is bake-list-day.

## Load order

1. `facts/MEMORY-INDEX.md` — which pairs exist and the entry format.
2. Shared pair: `facts/facts-shared.md` + `facts/rules-shared.md` (`Workflows: all`).
3. Operations pair: `facts/facts-operations.md` + `facts/rules-operations.md` (job-tagged or still holding legacy `all` entries).
4. Active Work Item: `work-items/<id>/facts/facts.md` and `rules.md` when present.

## Active Work Item

Read `.cursor/active-context.txt` (`work-item:<id>`). Legacy `.cursor/active-work-item.txt` is a read-only fallback. If still ambiguous, ask; do not invent a pack.

## Action triggers

Rules may carry `**Triggers:**`. The PreToolUse hook `.cursor/hooks/inject_rules_on_action.py` injects matching rule text from `facts/trigger-index.json`. Regenerate with `python scripts/memory/build_trigger_index.py` after retagging.

## What not to load

Do not load software-design or incident-bridge memory. Those are not this role.

## Health

Run `py -3 .cursor/skills/memory-optimize/scripts/analyze-memory.py facts` when files grow quickly. Warn if a file exceeds ~1,500 lines.
