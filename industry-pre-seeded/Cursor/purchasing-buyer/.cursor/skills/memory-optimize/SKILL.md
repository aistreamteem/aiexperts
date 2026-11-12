---
name: memory-optimize
description: Analyze and optimize the expert memory system for performance and maintainability
when_to_use: |
 - Quarterly health checks
 - After capturing many new facts/rules
 - When operations or shared memory files grow quickly
 - User explicitly requests memory optimization or health check
---

## Memory System Optimization Skill

Detects bloat, duplication, missing metadata, and weak navigation in this role’s Expert Role memory.

## Purpose

This role stores shop knowledge in:

- `facts/facts-operations.md` / `facts/rules-operations.md` (registered jobs)
- `facts/facts-shared.md` / `facts/rules-shared.md` (`Workflows: all`)
- `facts/MEMORY-INDEX.md`

Do not treat missing developer or incident-response files as errors. They are not used here.

## Quick health check

```bash
py -3 .cursor/skills/memory-optimize/scripts/analyze-memory.py facts
```

The script discovers every `facts/facts-*.md` and `facts/rules-*.md` on disk, counts dated entries (`##` or `### YYYY-MM-DD:`), and flags missing `**Workflows:**` metadata.

## Full analysis

1. File sizes and entry counts
2. Duplicate titles
3. Missing `**Workflows:**` or `**Triggers:**` on rules
4. MEMORY-INDEX still pointing at this role (operations + shared + registered jobs)

## Plan and execute

If issues exist, write a short plan and wait for operator approval before splitting or rewriting memory files. Preserve every entry. Split and index updates are done by hand: compare entry counts before and after; regenerate `facts/trigger-index.json` with `py -3 scripts/memory/build_trigger_index.py` after retagging rules. Split and index updates are done by hand; this scaffold has no separate split/update scripts.

## Healthy thresholds

- Prefer <1,500 lines per memory file
- `**Workflows:**` present on Expert Role entries
- Zero unintentional duplicate titles
- Index matches live files

## Maintenance

- After 10+ new entries in one session, run a metrics pass
- After promoting rules with non-`none` triggers, regenerate the trigger index
