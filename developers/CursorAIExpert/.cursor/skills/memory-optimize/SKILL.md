---
name: memory-optimize
description: Analyzes and optimizes the expert memory system for performance and maintainability. Use for a memory health check, after capturing many facts or rules, when memory files grow quickly, or when the user asks to optimize memory.
disable-model-invocation: false
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

**Execute an approved optimization plan** (agent does the split and index update by hand):
```
/memory-optimize --execute-phase=1
```

## Arguments

- `--metrics` - Quick health check only (file sizes, entry counts, metadata coverage)
- `--analyze-only` - Full analysis and generate plan without implementing (default)
- `--execute-phase=<N>` - Execute a specific phase of a previously approved plan
- `--full` - Run analysis → plan → implementation (requires approval before Phase 1)

## Workflow

### 1. Health Check (--metrics) and 2. Full Analysis

Run the analysis script (stdlib only). It discovers every `facts/facts-*.md` and `facts/rules-*.md` on disk:

```bash
py -3 .cursor/skills/memory-optimize/scripts/analyze-memory.py facts
```

**Health Thresholds**:
- File size: <1,000 lines per file (Warning: >1,500)
- Entries per file: <80 entries (Warning: >80)
- Workflow metadata: 100% coverage
- Duplication: Zero repeated entries

### 3. Generate Optimization Plan

If issues are detected, generate a phased optimization plan in `.cursor/plans/memory-optimization-YYYY-MM-DD.md`:

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

### 4. Execute Optimization (--execute-phase=N)

When the user approves the plan, the agent performs the split and the index update **by hand**. No split, index-update, or migration-validation script exists.

1. Record entry counts from a fresh `analyze-memory.py` run.
2. Split oversized files, consolidate duplicates, and backfill metadata as the plan says.
3. Update `facts/MEMORY-INDEX.md` to match the new structure.
4. Re-run `analyze-memory.py` and confirm the entry count matches the before count.
5. Regenerate the trigger index if any rules moved: `py -3 scripts/memory/build_trigger_index.py`.

**Key Lesson**: For files >1,000 lines, prefer scripted or carefully batched edits over one-shot manual rewriting so entry counts stay verifiable.

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
3. **Always get user approval before executing changes**
4. **Compare entry counts before and after** any split
5. **Commit optimization work separately** from feature development
6. **Archive original files** before major restructuring

## Automation Scripts

### analyze-memory.py

The only automation script. Path: `.cursor/skills/memory-optimize/scripts/analyze-memory.py`.

Detects issues: file bloat, duplication, missing metadata. Discovers `facts-*.md` / `rules-*.md` on disk.

Splitting files and updating `MEMORY-INDEX.md` are done by the agent by hand after plan approval.

## Example Invocations

**Quarterly check**:
```
/memory-optimize --metrics
```

**After major feature work**:
```
/memory-optimize
# Review generated plan in .cursor/plans/
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
- Analysis report: console + `facts/memory-analysis-YYYY-MM-DD.txt`
- Optimization plan: `.cursor/plans/memory-optimization-YYYY-MM-DD.md`
- Archives: `facts/*-ARCHIVE-YYYY-MM-DD.md`

## Success Criteria

After optimization:
- All files <1,000 lines (or <1,500 if justified)
- Entry count preserved (before/after compare confirms)
- 100% workflow metadata coverage
- Navigation index updated and accurate
- Zero unintentional duplicates
- Original files archived

---

**Version**: 1.1
**Next review**:
