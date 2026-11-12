# How Memory Loading Works

This landscaping-office Expert always loads **operations** memory for every registered job. Work Items are role packs (crew day, estimate, material pull, …), not software-build or outage workflows.

## Load order

1. `facts/MEMORY-INDEX.md`
2. `facts/facts-operations.md` and `facts/rules-operations.md`
3. `work-items/<id>/facts/` when a Work Item is active

## Active Work Item

1. Read `.cursor/active-context.txt` (`work-item:<id>`).
2. If missing, fall back to `.cursor/active-work-item.txt` (legacy read only).
3. Journals live under `journals/work-items/<id>/`; artifacts under `work-items/<id>/`.

## Triggers

Rules tagged with `**Triggers:**` are indexed by `scripts/memory/build_trigger_index.py` and surfaced by `.cursor/hooks/inject_rules_on_action.py` on matching writes (`write:csv`, `write:doc`).

## On-demand tools

Load `docs/tools/<name>.md` only when the current workflow step names that tool.
