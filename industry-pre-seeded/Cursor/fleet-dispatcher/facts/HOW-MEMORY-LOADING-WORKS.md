# How memory loading works

This expert keeps durable shop knowledge in markdown under `facts/`. Skills load a small set of files; the action hook can also inject matching rules when a file write is about to happen.

## What loads

1. Always read `facts/MEMORY-INDEX.md` first.
2. Always load the **shared** pair: `facts/facts-shared.md`, `facts/rules-shared.md` (`Workflows: all`).
3. Always load the **operations** pair: `facts/facts-operations.md`, `facts/rules-operations.md` (filter by registered job id when entries are tagged).
4. When a Work Item is active, also load `work-items/<id>/facts/facts.md` and `.../rules.md` if present.
5. Active journals come from hooks / `journals/` — not from inventing paths.

## Two axes

- **Workflow (browse):** which files to open for the current registered role job.
- **Triggers (action):** `**Triggers:**` on a rule, indexed by `python scripts/memory/build_trigger_index.py` into `facts/trigger-index.json`. The PreToolUse hook `.cursor/hooks/inject_rules_on_action.py` injects matching rule text for `write:doc` and `write:csv`.

## Active work item

Read `.cursor/active-context.txt` (`work-item:<id>`). The legacy `.cursor/active-work-item.txt` is a read-only fallback for older copies.

## Entry format

Use `### YYYY-MM-DD: Title` headers. See templates in `MEMORY-INDEX.md`. Rules need a `**Triggers:**` line (`write:doc`, `write:csv`, or `none`).
