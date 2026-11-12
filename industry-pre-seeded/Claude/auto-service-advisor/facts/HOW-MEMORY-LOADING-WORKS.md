# How Memory Loading Works

This role loads **shared** memory on every turn, then **operations** memory for service-advisor Work Items. There is no software-build or incident-response default.

## Discovery

1. Always load `facts/MEMORY-INDEX.md` first.
2. Always load the shared pair: `facts/facts-shared.md` + `facts/rules-shared.md`.
3. Load the operations pair: `facts/facts-operations.md` + `facts/rules-operations.md`.
4. Resolve the active Work Item from `.claude/active-context.txt` (legacy `.claude/active-work-item.txt` is read-only fallback).
5. If `work-items/<id>/facts/facts.md` or `rules.md` exist, load those too.
6. Load `docs/tools/<name>.md` and `.claude/workflows/<id>.md` only for the current step.

## Routing new captures

| Scope | Destination |
| --- | --- |
| Expert Role, `Workflows: all` | `facts/facts-shared.md` / `facts/rules-shared.md` |
| Expert Role, this shop's RO jobs | `facts/facts-operations.md` / `facts/rules-operations.md` |
| Work Item only | `work-items/<id>/facts/facts.md` / `rules.md` |

## Triggers

Rules that must fire on a tool action carry `**Triggers:**` (this role: `write:doc`, or `none`). The PreToolUse hook `.claude/hooks/inject_rules_on_action.py` reads `facts/trigger-index.json` built by `scripts/memory/build_trigger_index.py`.
