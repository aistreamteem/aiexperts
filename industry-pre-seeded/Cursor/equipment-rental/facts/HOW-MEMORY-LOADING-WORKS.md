# How Memory Loading Works

This Expert is an **equipment rental role**. Load operations memory for every Work Item. There is no developer, shared-split, or production-incident default.

## Mechanism

1. Always load `facts/MEMORY-INDEX.md` first.
2. Read `.cursor/active-context.txt` (`work-item:<id>`). Legacy `.cursor/active-work-item.txt` is a read-only fallback.
3. Load `facts/facts-operations.md` and `facts/rules-operations.md`.
4. If a Work Item is active, also load `work-items/<id>/facts/facts.md` and `rules.md` when present.
5. Filter Expert Role entries by `**Workflows:**` (`all` or the current registry job id).
6. Rules with a non-`none` `**Triggers:**` value are also indexed into `facts/trigger-index.json` for the PreToolUse hook (`.cursor/hooks/inject_rules_on_action.py`).

Tool docs under `docs/tools/` and workflow files under `.cursor/workflows/` load when the selected job names them.

## Maintenance

After adding or retagging a rule trigger, run:

```bash
py -3 scripts/memory/build_trigger_index.py
```

For health checks, run:

```bash
py -3 .cursor/skills/memory-optimize/scripts/analyze-memory.py facts
```
