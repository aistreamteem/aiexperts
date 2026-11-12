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

**Quick health check / full analysis:**
```
py -3 .claude/skills/memory-optimize/scripts/analyze-memory.py facts
```

**Execute an approved plan by hand** (there is no `split-and-optimize.py`, `update-index.py`, or `validate-migration.py`). Compare entry counts before and after any split, then update `facts/MEMORY-INDEX.md` yourself.

## Arguments

- `--metrics` / default analysis: run the script above
- Plan execution: agent edits files by hand after operator approval

## Workflow

### 1. Health Check

Run:
```
py -3 .claude/skills/memory-optimize/scripts/analyze-memory.py facts
```

**Health Thresholds**:
- File size: <1,000 lines per file (Warning: >1,500)
- Entries per file: <80 entries (Warning: >80)
- Workflow metadata: 100% coverage
- Duplication: Zero repeated entries

### 2. Full Analysis

Same command. The script scans every `facts/facts-*.md` and `facts/rules-*.md` on disk, reports sizes, entry counts, missing `**Workflows:**` metadata, and duplicate titles.

### 3. Generate Optimization Plan

If issues detected, write a phased plan in `.claude/plans/memory-optimization-YYYY-MM-DD.md` covering split, dedupe, metadata backfill, and index updates.

### 4. Execute Optimization

After approval:
1. Split or edit oversized files by hand (preserve entry count).
2. Backfill missing `**Workflows:**` / `**Triggers:**` fields.
3. Update `facts/MEMORY-INDEX.md` by hand.
4. Re-run the analyze script and confirm entry counts match before/after.

## Memory System Health Metrics

### Healthy Thresholds
- File size: <1,000 lines per file
- Section size: 5-15 entries per section
- Workflow metadata: 100% coverage
- Duplication: Zero repeated entries (except intentional cross-job copies)

### Warning Signs
- Files >1,500 lines
- Metadata coverage <80%
- 3+ duplicate entries

## Best Practices

1. Run the analyze script quarterly
2. Run it when facts/rules grow ~20%
3. Always get operator approval before restructuring
4. Compare entry counts before and after
5. Commit optimization work separately from pack work

## Output Location

- Health check / analysis: console
- Optimization plan: `.claude/plans/memory-optimization-YYYY-MM-DD.md`
- Archives: `facts/*-ARCHIVE-YYYY-MM-DD.md` when splitting

## Success Criteria

- All files <1,000 lines (or <1,500 if justified)
- Entry count preserved
- `MEMORY-INDEX.md` still points at shared and operations pairs
