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
/memory-optimize --metrics
```
or
```
/memory-optimize
```
or
```
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

### 1. Health Check and Full Analysis

Run the real analyzer (do not copy scripts into `facts/`):

```bash
py -3 .claude/skills/memory-optimize/scripts/analyze-memory.py facts
```

**Health Thresholds**:
- File size: <1,000 lines per file (Warning: >1,500)
- Entries per file: <80 entries (Warning: >80)
- Workflow metadata: 100% coverage
- Duplication: Zero repeated entries

### 2. Generate Optimization Plan

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

- [ ] Compare entry counts before and after (zero content loss)
- [ ] Verify file sizes within thresholds
- [ ] Check workflow metadata coverage
- [ ] Test navigation index links
```

### 3. Execute Optimization (--execute-phase=N)

When the operator approves the plan:

- **Split and reorganize** oversized `facts/facts-*.md` / `facts/rules-*.md` files by hand (or with a one-off edit). There is no `facts/split-and-optimize.py`.
- **Update the index** by editing `facts/MEMORY-INDEX.md` to match the files on disk. There is no `facts/update-index.py`.
- **Validate** by re-running `py -3 .claude/skills/memory-optimize/scripts/analyze-memory.py facts` and comparing entry counts before and after. There is no `validate-migration.py`.

## Memory System Health Metrics

### Healthy Thresholds
- File size: <1,000 lines per file
- Section size: 5-15 entries per section
- Workflow metadata: 100% coverage
- Duplication: Zero repeated entries (except intentional cross-workflow)
- Cross-references: Present in 30%+ of related entries

### Warning Signs
- Files >1,500 lines (context bloat risk)
- Sections >20 entries (discovery friction)
- Metadata coverage <80% (filtering broken)
- 3+ duplicate entries (maintenance debt)
- No index or navigation aids (scalability problem)

### Critical Issues
- Files >2,500 lines (agent efficiency severely degraded)
- No workflow-based splitting (all contexts polluted)
- 10+ duplicates (content divergence risk)
- Missing workflow-specific files

## Best Practices

1. **Run `--metrics` quarterly** (every 3 months)
2. **Run full analysis when facts/rules grow 20%**
3. **Always get operator approval before executing changes**
4. **Compare entry counts before and after** any split
5. **Commit optimization work separately** from feature work when this folder is under git
6. **Archive original files** before major restructuring

## Automation Scripts

### analyze-memory.py
Path: `.claude/skills/memory-optimize/scripts/analyze-memory.py`

Detects issues: file bloat, duplication, missing metadata. Discovers every `facts/facts-*.md` and `facts/rules-*.md` on disk.

Split, index update, and migration validation are done by the agent by hand — those helper scripts do not exist in this expert.

## Example Invocations

**Quarterly check**:
```
/memory-optimize --metrics
```

**After major pack work**:
```
/memory-optimize
# Review generated plan in .claude/plans/
# If approved:
/memory-optimize --execute-phase=1
```

## Maintenance Schedule

- **Weekly**: Monitor file sizes during active work
- **Monthly**: Check for obvious duplicates
- **Quarterly**: Run full `--metrics` health check
- **Annually**: Full optimization review (Phases 1-3)
- **Ad-hoc**: After 10+ facts/rules added in one session

## Output Location

- Health check: console output
- Analysis report: console + `facts/memory-analysis-YYYY-MM-DD.txt` (optional)
- Optimization plan: `.claude/plans/memory-optimization-YYYY-MM-DD.md`
- Archives: `facts/*-ARCHIVE-YYYY-MM-DD.md`

## Success Criteria

After optimization:
- All files <1,000 lines (or <1,500 if justified)
- Entry count preserved (before/after compare)
- 100% workflow metadata coverage
- Navigation index updated and accurate
- Zero unintentional duplicates
- Original files archived when restructuring

---

**Version**: 1.1
