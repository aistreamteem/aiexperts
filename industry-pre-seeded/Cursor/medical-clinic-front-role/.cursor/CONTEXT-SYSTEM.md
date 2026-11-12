# Active Context System

## Purpose

Tracks which **Work Item** (clinic role job) is active.

## Context File

- **Location:** `.cursor/active-context.txt`
- **Format:** `<type>:<id>`
- **Examples:**
  - `work-item:WID-21411151` (clinic day list, eligibility pack, referral paperwork)

## Context Types

### work-item

- **Purpose:** One isolated clinic front-role job
- **ID Format:** `WID-XXXXXXXX` or a dated pack name
- **Root Path:** `work-items/<id>/`
- **Journals:** `journals/work-items/<id>/progress.md` (flat), `journals/work-items/<id>/state.json`, `journals/work-items/<id>/nodes/`, `journals/work-items/<id>/agent-notes/`
- **Workflows:** registered role jobs in `.cursor/workflows/workflow-registry.json`

## Switching Context

User commands:
- `switch to work item WID-12345678` → writes `work-item:WID-12345678`

The agent will:
1. Parse the context file to determine type and ID
2. Route to `work-items/<id>/`
3. Load the Work Item journal, shared memory, and the selected workflow file

## Backward Compatibility

**Legacy file (read fallback only):** `.cursor/active-work-item.txt`  
Do not write this file. New work uses `.cursor/active-context.txt` only.

## Skill Integration

Skills that read context:
- **continue** — next ready work-map step
- **workflow-selector** — writes context when starting new work
- **journal-keeper** — journal paths
- **remember** / **promote-facts-rules** / **switch-context**

All skills should:
1. Read `.cursor/active-context.txt`
2. Parse format: `type:id`
3. Route `work-item` → `work-items/<id>/`

## Context Parsing Logic

```
Read .cursor/active-context.txt
If file doesn't exist:
- Check .cursor/active-work-item.txt (legacy read fallback)
- If exists: type=work-item, id=content
- If not exists: prompt user to start a new Work Item
Parse content as `type:id`
Set root_path = work-items/{id}/
Set journal_path = journals/work-items/{id}/progress.md
```

## Example Usage

```
**Starting a new day-list job:**
User: "start new work item WID-21411151"
Agent: writes `work-item:WID-21411151` to `.cursor/active-context.txt`
```
