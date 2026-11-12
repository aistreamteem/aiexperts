# How memory loading works

**Answer:** Load `facts/MEMORY-INDEX.md`, then this role’s **operations** pair. Work Items are hotel-role jobs (arrivals, due-outs, house count, and the other registered jobs).

## Load order

1. `facts/MEMORY-INDEX.md` (always first)
2. `facts/facts-operations.md` + `facts/rules-operations.md`
3. When a Work Item is active: `work-items/<id>/facts/facts.md` and `.../rules.md` if present

Filter Expert Role entries by `**Workflows:**` — include `all` or the current registry id.

## Active context

1. Read `.cursor/active-context.txt` (`work-item:<id>`)
2. Legacy read fallback: `.cursor/active-work-item.txt` (do not write it)
3. Default job if they decline to choose: `arrivals-day` (confirm first)

## Action triggers

Rules may carry `**Triggers:**` (`write:doc`, `write:csv`, `none`). The PreToolUse hook `.cursor/hooks/inject_rules_on_action.py` injects matching rule text from `facts/trigger-index.json`. Regenerate with `python scripts/memory/build_trigger_index.py`.

## What this role does not load

Developer, incident-response, or “shared” memory pairs are not part of this Expert. Operations memory is always loaded for every registered hotel-role job.
