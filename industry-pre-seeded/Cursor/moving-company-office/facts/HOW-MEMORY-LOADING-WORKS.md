# How Memory Loading Works

This role loads a small index, then the **shared** Expert Role pair, then the active Work Item’s own facts/rules.

## Load order

1. `facts/MEMORY-INDEX.md` — navigation and entry format
2. `facts/facts-shared.md` and `facts/rules-shared.md` — shop knowledge that applies across jobs (`**Workflows:** all` or a registry id)
3. `work-items/<id>/facts/facts.md` and `work-items/<id>/facts/rules.md` when present
4. Named `docs/tools/<name>.md` only when the current workflow step needs that tool

## Active work item

Read `.cursor/active-context.txt` (`work-item:<id>`). If missing, fall back to the legacy `.cursor/active-work-item.txt`, then the expert journal’s **Current work item** line.

## Filtering

Keep Expert Role entries whose `**Workflows:**` is `all` or matches the current registry id (for example `estimate-from-rate-file`, `crew-day`).

## Action triggers

Rules may carry `**Triggers:**` (`none`, `write:doc`, `write:csv`). The preToolUse hook `.cursor/hooks/inject_rules_on_action.py` injects matching rule text from `facts/trigger-index.json`. Regenerate with `python scripts/memory/build_trigger_index.py`.

## What this role does not load

Developer and incident-response memory pairs are not used here. Do not invent them for ordinary moving-office work.
