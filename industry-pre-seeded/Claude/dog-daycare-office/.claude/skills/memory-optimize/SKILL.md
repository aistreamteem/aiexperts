---
name: memory-optimize
description: Analyzes and optimizes the expert memory system for performance and maintainability. Use for a memory health check, after capturing many facts or rules, when memory files grow quickly, or when the user asks to optimize memory.
disable-model-invocation: false
---

## Memory System Optimization Skill

Detects bloat, duplication, missing metadata, and weak navigation in **this role’s shared Expert Role memory**.

## Purpose

This role stores shop knowledge in:

- `facts/facts-shared.md`
- `facts/rules-shared.md`
- `facts/MEMORY-INDEX.md`

Do not treat missing developer or incident-response files as errors. They are not used here.

## Quick health check

Run:

```bash
py -3 .claude/skills/memory-optimize/scripts/analyze-memory.py facts
```

The script discovers every `facts/facts-*.md` and `facts/rules-*.md` on disk, counts dated entries (`## YYYY-MM-DD:` or `### YYYY-MM-DD:`), and reports missing `**Workflows:**` metadata.

## Full analysis

1. File sizes and entry counts for shared facts/rules
2. Duplicate titles
3. Missing `**Workflows:**` or `**Triggers:**` on rules
4. MEMORY-INDEX still pointing at this role (shared + registered daycare/boarding jobs)

## Plan and execute

If issues exist, write a short plan under `.claude/plans/` and wait for operator approval before splitting or rewriting memory files. Preserve every entry. Split and index updates are done by the agent by hand: compare entry counts before and after, then regenerate `facts/TRIGGER-INDEX.md` with `python scripts/memory/build_trigger_index.py` when rule triggers change. Do not look for split/update/validate helper scripts under `facts/` — they are not part of this expert.

## Healthy thresholds

- Shared files: prefer <1,500 lines each
- `**Workflows:**` present on Expert Role entries
- Zero unintentional duplicate titles
- Index matches live files

## Maintenance

- After 10+ new entries in one session, run a metrics pass
- After promoting rules with non-`none` triggers, regenerate `facts/trigger-index.json`
