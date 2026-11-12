---
name: memory-optimize
description: Analyze and optimize the expert memory system for performance and maintainability
when_to_use: |
 - Quarterly health checks (every 3 months)
 - After capturing 10+ new facts/rules in a session
 - When memory files grow by 20%
 - When agent performance degrades (slow memory lookups, context bloat)
 - User explicitly requests memory optimization or health check
---

## Memory System Optimization Skill

Detects and resolves memory system issues: file bloat, duplication, poor organization, missing metadata, weak navigation.

## Usage

```
/memory-optimize --metrics
/memory-optimize
/memory-optimize --analyze-only
/memory-optimize --execute-phase=1
```

## Workflow

### 1. Health check / analysis

Run the real analyzer (do not copy scripts into `facts/`):

```bash
py -3 .claude/skills/memory-optimize/scripts/analyze-memory.py facts
```

Thresholds:
- File size: prefer under 1,000 lines (warn above 1,200; critical above 1,500)
- Entries per file: prefer under 80
- Workflow metadata: every entry should have `**Workflows:**`
- Duplication: avoid unintentional repeats

### 2. Generate an optimization plan

If issues are detected, write a short plan under `.claude/plans/memory-optimization-YYYY-MM-DD.md` listing critical/high/medium findings and the phases below. Get operator approval before changing files.

### 3. Execute (manual)

There is no `facts/split-and-optimize.py`, `facts/update-index.py`, or `validate-migration.py` in this expert. Split oversized files and update `facts/MEMORY-INDEX.md` by hand:

1. Count entries before the change (script output).
2. Move or edit entries carefully; keep `### YYYY-MM-DD: Title` headers.
3. Count entries after the change and confirm the total is unchanged (or explain intentional removals).
4. Regenerate the trigger index: `py -3 scripts/memory/build_trigger_index.py`.

### 4. Verification

- Re-run `analyze-memory.py facts`
- Confirm MEMORY-INDEX links still resolve
- Confirm rules that need action hooks still have `**Triggers:**`

## Best practices

1. Run `--metrics` quarterly.
2. Re-analyze after ~20% growth.
3. Always get approval before restructuring.
4. Compare entry counts before and after.
5. Commit memory maintenance separately from role-job packs when using git.
