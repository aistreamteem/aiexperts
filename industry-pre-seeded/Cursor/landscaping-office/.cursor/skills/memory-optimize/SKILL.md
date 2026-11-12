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

**Quick health check**:
```
/memory-optimize --metrics
```

**Full analysis with plan generation**:
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

### 1. Health Check (--metrics) and full analysis

Run the real analyzer (do not copy scripts into `facts/`):

```bash
py -3 .cursor/skills/memory-optimize/scripts/analyze-memory.py facts
```

**Health Thresholds**:
- File size: <1,000 lines per file (Warning: >1,500)
- Entries per file: <80 entries (Warning: >80)
- Workflow metadata: 100% coverage
- Duplication: Zero repeated entries

### 2. Generate Optimization Plan

If issues detected, generate a phased optimization plan in `.cursor/plans/memory-optimization-YYYY-MM-DD.md` covering split, dedupe, metadata backfill, and index updates.

### 3. Execute Optimization (--execute-phase=N)

When the operator approves a plan, apply the edits by hand (or with careful scripted transforms you write for that plan). There is no `split-and-optimize.py`, `update-index.py`, or `validate-migration.py` in this expert.

Compare entry counts from `analyze-memory.py` before and after. Update `facts/MEMORY-INDEX.md` by hand when sections move. Regenerate the trigger index after rule edits:

```bash
py -3 scripts/memory/build_trigger_index.py
```

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

1. Run the analyzer quarterly and after large memory growth
2. Always get operator approval before restructuring memory files
3. Compare entry counts before and after any split
4. Keep `facts/MEMORY-INDEX.md` and the trigger index in sync with the files on disk

## Analysis script

`.cursor/skills/memory-optimize/scripts/analyze-memory.py` — detects file bloat, duplication, missing metadata, and oversized entry counts across every `facts/facts-*.md` and `facts/rules-*.md`.

## Example Invocations

**Quarterly check**:
```
/memory-optimize --metrics
```

**After major feature work**:
```
# Captured 15 new facts/rules during WID-XXXXXXX
/memory-optimize
# Review generated plan in .cursor/plans/
# If approved:
/memory-optimize --execute-phase-1
```

**When memory feels slow**:
```
/memory-optimize
# Review findings and recommendations
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
- ✅ All files <1,000 lines (or <1,500 if justified)
- ✅ Entry count preserved (validation script confirms)
- ✅ 100% workflow metadata coverage
- ✅ Navigation index updated and accurate
- ✅ Zero unintentional duplicates
- ✅ Original files archived

---

**Version**: 1.0
**Next review**: 
