---
name: memory-optimize
description: Analyzes and optimizes the expert memory system for performance and maintainability. Use for a memory health check, after capturing many facts or rules, when memory files grow quickly, or when the user asks to optimize memory.
disable-model-invocation: false
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

Count lines and dated entries (`## YYYY-MM-DD:` or `### YYYY-MM-DD:`) in the shared pair. Warn if either file exceeds ~1,500 lines or if entries lack `**Workflows:**`.

Run:

```
py -3 .claude/skills/memory-optimize/scripts/analyze-memory.py facts
```

## Full analysis

1. File sizes and entry counts for shared facts/rules
2. Duplicate titles
3. Missing `**Workflows:**` or `**Triggers:**` on rules
4. MEMORY-INDEX still pointing at this role (shared + registered nonprofit-office jobs)

## Plan and execute

If issues exist, write a short plan and wait for operator approval before splitting or rewriting memory files. Preserve every entry. Do not migrate nonprofit-office content into developer buckets. The split and the index update are done by the agent by hand; compare entry counts before and after.

## Healthy thresholds

- Shared files: prefer <1,500 lines each
- `**Workflows:**` present on Expert Role entries
- Zero unintentional duplicate titles
- Index matches live files

## Maintenance

- After 10+ new entries in one session, run a metrics pass
- After promoting rules with non-`none` triggers, regenerate `facts/trigger-index.json`
