---
name: memory-optimize
description: Analyze and optimize the expert memory system for performance and maintainability
when_to_use: |
 - Quarterly health checks
 - After capturing many new facts/rules
 - When shared memory files grow quickly
 - User explicitly requests memory optimization or health check
---

## Memory System Optimization Skill

Detects bloat, duplication, missing metadata, and weak navigation in **this role’s shared memory**.

## Purpose

This role stores shop knowledge in:

- `facts/facts-shared.md`
- `facts/rules-shared.md`
- `facts/MEMORY-INDEX.md`

Do not treat missing developer or incident-response files as errors. They are not used here.

## Quick health check

Run:

```text
py -3 .cursor/skills/memory-optimize/scripts/analyze-memory.py facts
```

Warn if either shared file exceeds ~1,500 lines or if entries lack `**Workflows:**`. Entry headers are `### YYYY-MM-DD:` (or `##`).

## Full analysis

1. File sizes and entry counts for shared facts/rules (disk `facts-*.md` / `rules-*.md`)
2. Duplicate titles
3. Missing `**Workflows:**` or `**Triggers:**` on rules
4. MEMORY-INDEX still pointing at this role (shared pair + registered leasing jobs)

## Plan and execute

If issues exist, write a short plan under `.cursor/plans/` and wait for operator approval before splitting or rewriting memory files. Preserve every entry. Do not migrate leasing content into developer buckets. Split and index updates are done by the agent by hand; compare entry counts before and after.

## Healthy thresholds

- Shared files: prefer <1,500 lines each
- `**Workflows:**` present on Expert Role entries
- Zero unintentional duplicate titles
- Index matches live files

## Maintenance

- After 10+ new entries in one session, run a metrics pass
- After promoting rules with non-`none` triggers, regenerate `facts/trigger-index.json`
