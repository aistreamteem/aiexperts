---
name: memory-optimize
description: Analyze and optimize the childcare-office operations memory files for performance and maintainability
when_to_use: |
 - Quarterly health checks
 - After capturing 10+ new facts/rules in a session
 - When operations memory files grow by 20%
 - User explicitly requests memory optimization or health check
---

## Memory System Optimization Skill

Detects and resolves memory issues in **this role’s operations files**: bloat, duplication, missing metadata, weak navigation.

## Purpose

Maintain `facts/facts-shared.md`, `facts/rules-shared.md`, `facts/facts-operations.md`, `facts/rules-operations.md`, and `facts/MEMORY-INDEX.md`. Software-build and incident-response memory files are **not** part of this role; missing those files is not an error.

## Usage

**Quick health check**: `/memory-optimize --metrics`  
**Full analysis**: `/memory-optimize`  
**Execute approved plan**: `/memory-optimize --execute-phase=N`

## Health check files

Only these are required:

- `facts/facts-shared.md`
- `facts/rules-shared.md`
- `facts/facts-operations.md`
- `facts/rules-operations.md`
- `facts/MEMORY-INDEX.md`

Optional: `facts/HOW-MEMORY-LOADING-WORKS.md`

Count entries (`### YYYY-MM-DD:` headings), line counts, missing `**Workflows:**`, duplicate titles.

Run: `py -3 .cursor/skills/memory-optimize/scripts/analyze-memory.py facts`

Split oversized files and refresh MEMORY-INDEX by hand; compare entry counts before and after.

**Thresholds:**
- Warning: a file >1,500 lines or >80 entries
- Missing software-build or SEV-bridge files: ignore
- Duplication: flag titles that appear more than twice

## Analysis

Use `.cursor/skills/memory-optimize/scripts/analyze-memory.py` when present. Only operations files are required; other split files are skipped, not CRITICAL.

If issues exist, write a plan to `.cursor/plans/memory-optimization-YYYY-MM-DD.md` with phases:

1. Structural (split only if operations files are oversized)
2. Content (section size, starter-vs-taught labels)
3. Maintenance (MEMORY-INDEX pointers for this role’s workflows)

Get operator approval before executing. Archive originals before a large rewrite.

## Success

- Operations files remain the live memory
- Entry count preserved
- MEMORY-INDEX still leads with this childcare-office role
