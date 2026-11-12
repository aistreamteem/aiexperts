# How memory loading works

This expert keeps a small, file-based memory. There is no vector store.

## Files

| Kind | Path |
| --- | --- |
| Index | `facts/MEMORY-INDEX.md` |
| Shared facts | `facts/facts-shared.md` |
| Shared rules | `facts/rules-shared.md` |
| Trigger index | `facts/TRIGGER-INDEX.md` + `facts/trigger-index.json` |
| Work Item memory | `work-items/<id>/facts/facts.md` and `rules.md` when present |

`Workflows: all` entries live in the shared pair so every registered staffing-office job loads them.

## Load order

1. Read `.claude/active-context.txt` (legacy fallback: `.claude/active-work-item.txt`)
2. `facts/MEMORY-INDEX.md`
3. `facts/facts-shared.md` and `facts/rules-shared.md`
4. `work-items/<id>/facts/` when present
5. Filter Expert Role entries by `**Workflows:**` (`all` or the current registry id)

## Action triggers

Rules may carry `**Triggers:**` (`none`, `write:doc`, `write:csv`). The PreToolUse hook `.claude/hooks/inject_rules_on_action.py` injects matching rule bodies from `trigger-index.json` when those actions run.

Regenerate the index after retagging:

```text
python scripts/memory/build_trigger_index.py
```

## Capture

- One-off: **remember**
- Batch docs: **integrate-docs**
- Promote Work Item notes: **promote-facts-rules**
- Health check: **memory-optimize** (`py -3 .claude/skills/memory-optimize/scripts/analyze-memory.py facts`)
