# Active Context System

## Purpose

Tracks which **Work Item** (janitorial-office role job) is active.

## Context File

- **Location:** `.claude/active-context.txt`
- **Format:** `<type>:<id>`
- **Examples:**
  - `work-item:WID-214111151`
  - `work-item:2026-09-15-clinic-night`

## Context Types

### work-item

- **Purpose:** One isolated janitorial-office job
- **ID Format:** `WID-XXXXXXXX` or a pack/site-night name
- **Root Path:** `work-items/<id>/`
- **Journals:** `journals/work-items/<id>/progress.md` (flat), `journals/work-items/<id>/state.json`, `journals/work-items/<id>/nodes/`
- **Workflows:** registered role jobs in `.claude/workflows/workflow-registry.json`

## Switching Context

User commands:
- `switch to work item WID-12345678` → writes `work-item:WID-12345678`

The agent will:
1. Parse the context file to determine type and ID
2. Route to `work-items/<id>/`
3. Load the Work Item journal, operations memory, and the selected workflow file

## Backward Compatibility

**Legacy file (read fallback only):** `.claude/active-work-item.txt`. Do not write it.

## Skill Integration

Skills that read context:
- **continue** — next ready workflow step
- **workflow-selector** — writes context when starting new work
- **journal-keeper** — journal paths
- **remember** / **promote-facts-rules** / **switch-context**

All skills should:
1. Read `.claude/active-context.txt`
2. Parse format: `type:id`
3. Route `work-item` → `work-items/<id>/`

## Context Parsing Logic

```
Read .claude/active-context.txt
If file doesn't exist:
- Check .claude/active-work-item.txt (legacy)
- If exists: type=work-item, id=content
- If not exists: prompt user to start a new Work Item
Parse content as `type:id`
Set root_path = work-items/{id}/
Set journal_path = journals/work-items/{id}/progress.md
Set map_path = journals/work-items/{id}/state.json
```

## Example Usage

```
**Starting a new night-board job:**
User: "start new work item 2026-09-15-clinic-night"
Agent: writes `work-item:2026-09-15-clinic-night` to `.claude/active-context.txt`
```
