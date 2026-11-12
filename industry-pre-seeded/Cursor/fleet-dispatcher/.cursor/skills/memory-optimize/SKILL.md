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
- Generating optimization plans when issues are detected

## Usage

**Health check / analysis** — run the real analyzer (do not copy scripts into `facts/`):

```bash
py -3 .cursor/skills/memory-optimize/scripts/analyze-memory.py facts
```

**Execute an approved plan** — split oversized files and refresh `facts/MEMORY-INDEX.md` by hand (or with agent edits). Compare entry counts from the analyzer before and after. This scaffold has no separate split/index/validate scripts under facts/; the agent does those edits directly.

## Workflow

### 1. Health Check

Run the analyzer command above. Review file sizes, entry counts, missing `**Workflows:**` metadata, and duplicate titles.

**Health Thresholds**:

- File size: <1,000 lines per file (Warning: >1,500)
- Entries per file: <80 entries (Warning: >80)
- Workflow metadata: 100% coverage
- Duplication: Zero repeated entries

### 2. Generate Optimization Plan

If issues are detected, write a phased plan under `.cursor/plans/memory-optimization-YYYY-MM-DD.md` covering structural splits, content cleanup, and index maintenance. Get operator approval before changing live memory files.

### 3. Execute

- Split or trim oversized facts/rules files under facts/ by hand (facts-shared, facts-operations, rules-shared, rules-operations).
- Keep `### YYYY-MM-DD: Title` headers and metadata fields intact.
- Update `facts/MEMORY-INDEX.md` navigation when files change.
- Re-run the analyzer and confirm entry counts did not drop unexpectedly.
- Regenerate the trigger index after rule edits: `python scripts/memory/build_trigger_index.py`.

## Best Practices

1. Run the analyzer quarterly and after large capture sessions.
2. Always get operator approval before restructuring memory.
3. Prefer the shared pair for `Workflows: all` and the operations pair for registered role jobs.
4. Commit memory maintenance separately from pack work when using git.

## Output Location

- Health check: console output from `analyze-memory.py`
- Optimization plan: `.cursor/plans/memory-optimization-YYYY-MM-DD.md`
