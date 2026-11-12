---
name: memory-optimize
description: Analyze and optimize the expert memory system for performance and maintainability
when_to_use: |
 - Quarterly health checks (every 3 months)
 - After capturing 10+ new facts/rules in a session
 - When memory files grow by 20% (e.g., 1,300 → 1,560 lines)
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

**Execute an approved optimization plan**:
Do the split and the MEMORY-INDEX update by hand (or with small focused edits). Compare entry counts before and after with the same analyze command. There is no `facts/split-and-optimize.py`, `facts/update-index.py`, or `validate-migration.py` in this scaffold.

## Arguments (when invoked as a skill)

- `--metrics` / default analyze: run `analyze-memory.py` and report findings
- `--execute-phase=<N>`: apply an already approved plan from `.claude/plans/` by editing the memory files directly; re-run analyze afterward

## Workflow

### 1. Health Check

```bash
py -3 .claude/skills/memory-optimize/scripts/analyze-memory.py facts
```

The script discovers every `facts/facts-*.md` and `facts/rules-*.md` on disk. Entry headers match `##` or `### YYYY-MM-DD: Title`.

**Health Thresholds**:
- File size: <1,000 lines per file (Warning: >1,500)
- Entries per file: <80 entries (Warning: >80)
- Workflow metadata: 100% coverage
- Duplication: Zero repeated entries

### 2. Full Analysis

Run the same command. Use the printed report (file sizes, entry counts, missing `**Workflows:**` metadata, duplicates) to decide whether an optimization plan is needed.

### 3. Generate Optimization Plan

If issues are detected, write a phased plan to `.claude/plans/memory-optimization-YYYY-MM-DD.md`:

```markdown
# Memory Optimization Plan

**Date**: YYYY-MM-DD
**Trigger**: [quarterly check | 20% growth | performance degradation | user request]

## Issues Detected

[List of critical/high/medium issues from analysis]

## Phase 1: Structural (if critical issues)

- [ ] Split oversized files (>1,500 lines)
- [ ] Consolidate duplicates
- [ ] Backfill missing workflow metadata

## Phase 2: Content (if high issues)

- [ ] Break up oversized sections (>15 entries)
- [ ] Standardize procedure formats
- [ ] Add cross-references

## Phase 3: Maintenance (if medium issues)

- [ ] Update MEMORY-INDEX.md
- [ ] Add section summaries
- [ ] Verify navigation links
- [ ] Regenerate trigger index: `py -3 scripts/memory/build_trigger_index.py`

## Verification

- [ ] Entry count before == entry count after
- [ ] File sizes within thresholds
- [ ] Workflow metadata coverage
- [ ] Test MEMORY-INDEX / TRIGGER-INDEX links
```

### 4. Execute Optimization

When the user approves the plan:

1. Record entry counts from `analyze-memory.py`.
2. Edit the memory files by hand (move, split, dedupe, backfill metadata).
3. Update `facts/MEMORY-INDEX.md` and run `py -3 scripts/memory/build_trigger_index.py`.
4. Re-run `analyze-memory.py` and confirm entry counts match.

## Memory System Health Metrics

### Healthy Thresholds
- File size: <1,000 lines per file
- Section size: 5-15 entries per section
- Workflow metadata: 100% coverage
- Duplication: Zero repeated entries (except intentional cross-workflow)
- Cross-references: Present in 30%+ of related entries

### Warning Signs
- Files >1,500 lines
- Sections >20 entries
- Metadata coverage <80%
- 3+ duplicate entries
- No index or navigation aids

### Critical Issues
- Files >2,500 lines
- No workflow-based splitting
- 10+ duplicates
- Missing workflow-specific or shared files

## Best Practices

1. Run the analyze script quarterly
2. Run it when facts/rules grow ~20%
3. Always get user approval before restructuring
4. Compare entry counts before and after
5. Commit optimization work separately from feature development

## Automation

The only automation script shipped with this skill is:

```bash
py -3 .claude/skills/memory-optimize/scripts/analyze-memory.py facts
```

Split, index update, and migration validation are done by the agent (and the trigger-index builder), not by separate facts/*.py scripts.

## Output Location

- Health check / analysis: console output
- Optimization plan: `.claude/plans/memory-optimization-YYYY-MM-DD.md`

## Success Criteria

After optimization:
- All files <1,000 lines (or <1,500 if justified)
- Entry count preserved
- 100% workflow metadata coverage
- Navigation / trigger indexes updated
- Zero unintentional duplicates
