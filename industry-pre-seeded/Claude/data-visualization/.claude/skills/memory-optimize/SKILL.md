---
name: memory-optimize
description: Analyze and optimize the expert memory system for performance and maintainability
when_to_use: |
  - Quarterly health checks (every 3 months)
  - After capturing 10+ new facts/rules in a session
  - When operations memory files grow by 20%
  - When agent performance degrades (slow memory lookups, context bloat)
  - User explicitly requests memory optimization or health check
---

## Memory System Optimization Skill

Detects and resolves memory system issues: file bloat, duplication, poor organization, missing metadata, weak navigation.

This role’s live memory is the **shared** pair plus the **operations** pair under `facts/`. Missing developer or incident files are expected and are not errors.

## Purpose

Maintain expert memory system health by:
- Monitoring file sizes and entry counts
- Detecting content duplication
- Verifying workflow metadata coverage
- Identifying oversized sections
- Generating optimization plans when issues detected

## Usage

**Quick health check**: `/memory-optimize --metrics`

**Full analysis**: `/memory-optimize` or `/memory-optimize --analyze-only`

**Execute approved plan**: `/memory-optimize --execute-phase=1`

## Workflow

### 1. Health Check (--metrics)

Count entries in every `facts/facts-*.md` and `facts/rules-*.md` on disk.

Use `py -3 .claude/skills/memory-optimize/scripts/analyze-memory.py facts`. Missing files for other roles are expected and are not errors.

**Health Thresholds**:
- File size: <1,000 lines per file (Warning: >1,500)
- Entries per file: warning >80
- Workflow metadata: 100% coverage
- Duplication: Zero unintentional repeated entries

### 2. Full Analysis

Run the same script for duplicates, missing `**Workflows:**`, and oversized files. Write a report to `facts/memory-analysis-YYYY-MM-DD.txt` when useful.

### 3. Generate Optimization Plan

If issues exist, write `.claude/plans/memory-optimization-YYYY-MM-DD.md` with phases: split oversized operations files, consolidate duplicates, backfill metadata, update MEMORY-INDEX.

### 4. Execute Optimization

Only after operator approval. Preserve entry count. Archive originals under `facts/*-ARCHIVE-YYYY-MM-DD.md` before a major split.

## Best Practices

1. Run `--metrics` quarterly
2. Get user approval before executing changes
3. Use Python scripts for files >1,000 lines
4. Validate zero content loss
5. Keep routing on shared + operations; do not create developer/incident splits for this role

## Success Criteria

- Operations files within thresholds (or justified)
- Entry count preserved
- MEMORY-INDEX accurate
- Zero unintentional duplicates
