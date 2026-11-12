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

## Purpose

Maintain expert memory system health by:
- Monitoring file sizes and entry counts
- Detecting content duplication
- Verifying workflow metadata coverage
- Identifying oversized sections
- Generating optimization plans when issues detected

## Usage

**Quick health check / full analysis**:
```
py -3 .claude/skills/memory-optimize/scripts/analyze-memory.py facts
```

**Execute an approved optimization plan** by editing memory files by hand (or with operator approval). There is no `split-and-optimize.py`, `update-index.py`, or `validate-migration.py` in this scaffold — split oversized files and refresh `facts/MEMORY-INDEX.md` yourself, comparing entry counts before and after.

## Arguments (skill invocation)

- `--metrics` / default analyze — run the script above and report
- `--execute-phase=<N>` — apply an approved plan phase manually; re-run the script to verify

## Workflow

### 1. Health Check

```bash
py -3 .claude/skills/memory-optimize/scripts/analyze-memory.py facts
```

**Health Thresholds**:
- File size: <1,000 lines per file (Warning: >1,500)
- Entries per file: <80 entries (Warning: >80)
- Workflow metadata: 100% coverage
- Duplication: Zero repeated entries

### 2. Full Analysis

Run the same command. The script lists every `facts/facts-*.md` and `facts/rules-*.md` on disk, counts `##` / `### YYYY-MM-DD:` entries, and reports missing `**Workflows:**` metadata and duplicate titles.

### 3. Generate Optimization Plan

If issues are detected, write a phased plan in `.claude/plans/memory-optimization-YYYY-MM-DD.md` covering split, dedupe, metadata backfill, and index refresh.

### 4. Execute Optimization

With operator approval:
1. Count entries before changes (script output).
2. Split or edit memory files by hand.
3. Update `facts/MEMORY-INDEX.md` by hand.
4. Re-run the analysis script and confirm entry counts match.

## Memory System Health Metrics

### Healthy Thresholds
- File size: <1,000 lines per file
- Section size: 5-15 entries per section
- Workflow metadata: 100% coverage
- Duplication: Zero repeated entries (except intentional cross-workflow)

### Warning Signs
- Files >1,500 lines
- Sections >20 entries
- Metadata coverage <80%
- 3+ duplicate entries

## Best Practices

1. Run the analysis script quarterly
2. Run it when facts/rules grow ~20%
3. Always get operator approval before restructuring
4. Compare entry counts before and after
5. Keep optimization commits separate from pack work

## Automation

Only `scripts/analyze-memory.py` (under this skill) exists. Splits and index updates are manual agent work.

## Output Location

- Health check / analysis: console
- Optimization plan: `.claude/plans/memory-optimization-YYYY-MM-DD.md`

## Success Criteria

- All files within size thresholds (or justified)
- Entry count preserved
- 100% workflow metadata coverage
- Navigation index accurate
- Zero unintentional duplicates
