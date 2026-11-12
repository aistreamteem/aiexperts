# How Memory Loading Works

Load the index, then shared memory, then this role’s operations pair, then the active Work Item memory.

## Discovery

1. Always load `facts/MEMORY-INDEX.md` first.
2. Always load `facts/facts-shared.md` and `facts/rules-shared.md`.
3. Load `facts/facts-operations.md` and `facts/rules-operations.md` for registered purchasing jobs. Filter by `**Workflows:**` (`all` or the current registry key).
4. Load `work-items/<id>/facts/facts.md` and `.../rules.md` when present (no workflow filter).

## Active pack

1. Read `.claude/active-context.txt` (legacy read fallback: `.claude/active-work-item.txt`).
2. Read `journals/work-items/<id>/progress.md` for **Workflow type**.
3. If missing, run **workflow-selector** (default `avl-check`).

## On demand

Load `docs/tools/<name>.md` when a workflow step cites it. Load `docs/role/work-item-method.md` when choosing or explaining phases.

## Action triggers

Rules tagged with a real trigger (for example `write:doc`, `write:csv`, `write:pack`) are also indexed in `TRIGGER-INDEX.md` / `trigger-index.json` for the PreToolUse hook `.claude/hooks/inject_rules_on_action.py`. Regenerate with `py -3 scripts/memory/build_trigger_index.py`.

## Maintenance

Run **memory-optimize** (`py -3 .claude/skills/memory-optimize/scripts/analyze-memory.py facts`). Prefer under ~1,500 lines per memory file.
