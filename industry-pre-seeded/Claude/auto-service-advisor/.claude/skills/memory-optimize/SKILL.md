---
name: memory-optimize
disable-model-invocation: false
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
/memory-optimize --metrics
/memory-optimize
/memory-optimize --analyze-only
```

**Execute approved optimization plan**:
```
/memory-optimize --execute-phase=1
```

## Arguments

- `--metrics` - Quick health check only (file sizes, entry counts, metadata coverage)
- `--analyze-only` - Full analysis and generate plan without implementing (default)
- `--execute-phase=<N>` - Execute specific phase of previously approved plan
- `--full` - Run analysis → plan → implementation (requires approval before Phase 1)

## Workflow

### 1. Health Check (--metrics) and 2. Full Analysis

Run the real analyzer (do not copy scripts into `facts/`):

```bash
py -3 .claude/skills/memory-optimize/scripts/analyze-memory.py facts
```

**Health Thresholds**:
- File size: <1,000 lines per file (Warning: >1,500)
- Entries per file: <80 entries (Warning: >80)
- Workflow metadata: 100% coverage
- Duplication: Zero repeated entries

### 3. Generate Optimization Plan

If issues detected, generate a phased optimization plan in `.claude/plans/memory-optimization-YYYY-MM-DD.md`:

**Plan Template**:
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

## Expected Outcomes

[Performance improvements, file size reductions, etc.]

## Verification

- [ ] Compare entry counts before and after (agent does this by hand)
- [ ] Verify file sizes within thresholds
- [ ] Check workflow metadata coverage
- [ ] Test navigation index links
```

### 4. Execute Optimization (--execute-phase=N)

When the operator approves the plan:

- Split oversized files and consolidate duplicates **by hand** (or with a one-off edit the agent writes for this run). There is no `facts/split-and-optimize.py`.
- Update `facts/MEMORY-INDEX.md` by hand. There is no `facts/update-index.py`.
- Compare entry counts from `analyze-memory.py` before and after. There is no `validate-migration.py`.
- After retagging rules, run `python scripts/memory/build_trigger_index.py`.

## Memory System Health Metrics

### Healthy Thresholds
- File size: <1,000 lines per file
- Section size: 5-15 entries per section
- Workflow metadata: 100% coverage
- Duplication: Zero repeated entries (except intentional cross-file)

### Warning Signs
- Files >1,500 lines (context bloat risk)
- Sections >20 entries (discovery friction)
- Metadata coverage <80% (filtering broken)
- 3+ duplicate entries (maintenance debt)

### Critical Issues
- Files >2,500 lines (agent efficiency severely degraded)
- 10+ duplicates (content divergence risk)

## Best Practices

1. Run `--metrics` quarterly (every 3 months)
2. Run full analysis when facts/rules grow 20%
3. Always get operator approval before executing changes
4. Validate zero content loss after optimization (entry count before = after)
5. Commit optimization work separately from RO-pack work
6. Archive original files before major restructuring

## Automation Scripts

### analyze-memory.py

Path: `.claude/skills/memory-optimize/scripts/analyze-memory.py`

Detects issues: file bloat, duplication, missing metadata. Scans every `facts/facts-*.md` and `facts/rules-*.md` on disk.

Split and index updates are done by the agent by hand; only this analyzer is shipped.

## Example Invocations

```
/memory-optimize --metrics
/memory-optimize
```

## Output Location

- Health check: console output
- Analysis report: console + optional `facts/memory-analysis-YYYY-MM-DD.txt`
- Optimization plan: `.claude/plans/memory-optimization-YYYY-MM-DD.md`
- Archives: `facts/*-ARCHIVE-YYYY-MM-DD.md`

## Success Criteria

After optimization:
- All files <1,000 lines (or <1,500 if justified)
- Entry count preserved
- 100% workflow metadata coverage
- Navigation index updated and accurate
- Zero unintentional duplicates
- Original files archived when restructuring
