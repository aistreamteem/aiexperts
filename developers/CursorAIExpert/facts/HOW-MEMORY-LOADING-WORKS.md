# How memory loading works

Short description of the expert memory mechanism in this scaffold. Entry format lives in [MEMORY-INDEX.md](MEMORY-INDEX.md).

## Two axes

1. **Workflow axis (browse / context budget).** Skills load a **shared** pair (`facts-shared.md`, `rules-shared.md`) plus the pair for the current workflow (e.g. `facts-developer.md`, `rules-developer.md`). Work Item memory lives under `work-items/<id>/facts/`. Entries marked `Workflows: all` are filed in the shared pair so every workflow sees them.
2. **Trigger axis (action-time).** Rules may carry a `**Triggers:**` field. `scripts/memory/build_trigger_index.py` builds `TRIGGER-INDEX.md` and `trigger-index.json`. The preToolUse hook `.cursor/hooks/inject_rules_on_action.py` injects matching rule text when the agent is about to take that action, in any workflow.

## What loads when

| Moment | What is loaded |
| --- | --- |
| Session start / before prompt / preToolUse | Journal context via `inject_journal_context.py` (expert journal, flat work-item journal, active branch notes) |
| Skill start (continue, spec-parser, implement, iterative) | `MEMORY-INDEX.md`, shared pair, workflow pair, then Work Item `facts/` |
| About to Write/Shell a matching action | Rules whose Triggers match, from `trigger-index.json` |

## Active work item

The active id is the line in `.cursor/active-context.txt` (`work-item:<id>`). Hooks and skills may read the legacy `.cursor/active-work-item.txt` as a fallback; nothing writes that file any more.

## Files on disk

- Expert: `facts/facts-*.md`, `facts/rules-*.md` (discoverable by glob; create an incident-response pair when that workflow is enabled)
- Indexes: `MEMORY-INDEX.md`, `TRIGGER-INDEX.md`, `trigger-index.json`
- Work Item: `work-items/<id>/facts/facts.md`, `work-items/<id>/facts/rules.md`

## Maintenance

- Capture with the **remember** skill; promote with **promote-facts-rules**
- Health check: `py -3 .cursor/skills/memory-optimize/scripts/analyze-memory.py facts`
- After retagging rules: `py -3 scripts/memory/build_trigger_index.py`
