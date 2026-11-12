---
name: memory-optimize
description: Analyze and optimize the expert memory system for performance and maintainability
when_to_use: |
 - Quarterly health checks
 - After capturing many new facts/rules
 - When clinic memory files grow quickly
 - User explicitly requests memory optimization or health check
---

## Memory System Optimization Skill

Detects bloat, duplication, missing metadata, and weak navigation in **this role’s clinic memory**.

## Purpose

This role stores shop knowledge in:

- `facts/facts-shared.md` / `facts/rules-shared.md`
- `facts/MEMORY-INDEX.md`

Do not treat missing developer or incident-response files as errors. They are not used here.

## Quick health check

```bash
py -3 .cursor/skills/memory-optimize/scripts/analyze-memory.py facts
```

Count lines and dated entries (`## YYYY-MM-DD:` or `### YYYY-MM-DD:`) in the shared pair. Warn if a file exceeds ~1,500 lines or if entries lack `**Workflows:**`.

## Full analysis

1. File sizes and entry counts for `facts/facts-*.md` and `facts/rules-*.md` on disk
2. Duplicate titles
3. Missing `**Workflows:**` or `**Triggers:**` on rules
4. MEMORY-INDEX still pointing at this role (shared + registered clinic jobs)

## Plan and execute

If issues exist, write a short plan under `.cursor/plans/` and wait for operator approval before splitting or rewriting memory files. Preserve every entry. Compare entry counts before and after by hand. Do not migrate clinic content into developer buckets. There is no `facts/split-and-optimize.py`, `facts/update-index.py`, or `validate-migration.py` — the agent updates MEMORY-INDEX and files manually after approval.

## Healthy thresholds

- Memory files: prefer <1,500 lines each
- `**Workflows:**` present on Expert Role entries
- Zero unintentional duplicate titles
- Index matches live files

## Maintenance

- After 10+ new entries in one session, run a metrics pass
- After promoting rules with non-`none` triggers, regenerate `facts/trigger-index.json` with `py -3 scripts/memory/build_trigger_index.py`
