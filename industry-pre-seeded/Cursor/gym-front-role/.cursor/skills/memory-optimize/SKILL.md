---
name: memory-optimize
description: Analyze and optimize the expert memory system for performance and maintainability
when_to_use: |
 - Quarterly health checks
 - After capturing many new facts/rules
 - When operations memory files grow quickly
 - User explicitly requests memory optimization or health check
---

## Memory System Optimization Skill

Detects bloat, duplication, missing metadata, and weak navigation in **this role’s operations memory**.

## Purpose

This role stores shop knowledge in:

- `facts/facts-operations.md`
- `facts/rules-operations.md`
- `facts/MEMORY-INDEX.md`

Do not treat missing developer or incident-response files as errors. They are not used here.

## Quick health check

Count lines and dated entries (`## YYYY-MM-DD:` or `### YYYY-MM-DD:`) in the operations pair. Warn if either file exceeds ~1,500 lines or if entries lack `**Workflows:**`.

You may use `.cursor/skills/memory-optimize/scripts/analyze-memory.py` after pointing it at the operations files only.

## Full analysis

1. File sizes and entry counts for operations facts/rules
2. Duplicate titles
3. Missing `**Workflows:**` or `**Triggers:**` on rules
4. MEMORY-INDEX still pointing at this role (operations + registered gym-role jobs)

## Plan and execute

If issues exist, write a short plan under `.cursor/plans/` and wait for operator approval before splitting or rewriting memory files. Preserve every entry. Do not migrate gym-role content into developer buckets.

## Healthy thresholds

- Operations files: prefer <1,500 lines each
- `**Workflows:**` present on Expert Role entries
- Zero unintentional duplicate titles
- Index matches live files

## Maintenance

- After 10+ new entries in one session, run a metrics pass
- After promoting rules with non-`none` triggers, regenerate `facts/trigger-index.json`
