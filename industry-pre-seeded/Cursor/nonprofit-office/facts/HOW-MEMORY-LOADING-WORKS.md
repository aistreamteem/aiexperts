# How Memory Loading Works

Load a small index, then this role’s **shared** pair, then the active Work Item’s own facts/rules.

## Discovery

1. Read `facts/MEMORY-INDEX.md` first.
2. Read `.cursor/active-context.txt` (legacy `.cursor/active-work-item.txt` is read-only fallback).
3. Load `facts/facts-shared.md` and `facts/rules-shared.md` on every Work Item.
4. Load `work-items/<id>/facts/facts.md` and `rules.md` when present.
5. Filter Expert Role entries whose `**Workflows:**` is `all` or matches the current registry id.
6. Load `docs/tools/<name>.md` only when the current YAML step names that tool.

## Why shared (not operations / developer / incident)

This expert is one nonprofit-office role. Entries marked `Workflows: all` live in the shared pair so every registered job loads them. Do not invent developer or incident-response memory files for this role.

## Maintenance

- Capture with **remember**; promote with **promote-facts-rules**.
- After retagging a rule’s Triggers, run `python scripts/memory/build_trigger_index.py`.
- Use **memory-optimize** (`py -3 .cursor/skills/memory-optimize/scripts/analyze-memory.py facts`) when files grow large.
