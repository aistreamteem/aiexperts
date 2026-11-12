# Active Context System

## Purpose

Tracks which **Work Item** (hotel-role job) is active.

## Context File

- **Location:** `.cursor/active-context.txt`
- **Format:** `<type>:<id>`
- **Examples:**
  - `work-item:WID-20261108` (today’s arrivals list, a folio-exception pack, a group-block comparison)

## Context Types

### work-item

- **Purpose:** One isolated hotel / inn front-role job
- **ID Format:** `WID-XXXXXXXX`
- **Root Path:** `work-items/<id>/`
- **Journals:** `journals/work-items/<id>/progress.md` (flat), `journals/work-items/<id>/state.json`, `journals/work-items/<id>/nodes/`
- **Agent notes:** `journals/work-items/<id>/agent-notes/`
- **Workflows:** registered role jobs in `.cursor/workflows/workflow-registry.json`

## Switching Context

User commands:
- `switch to work item WID-12345678` → writes `work-item:WID-12345678`

The agent will:
1. Parse the context file to determine type and ID
2. Route to `work-items/<id>/`
3. Load the Work Item journal, operations memory, and the selected workflow file

## Backward Compatibility

**Legacy read fallback only:** `.cursor/active-work-item.txt` (hooks may still read it; skills must not write it).

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
- Check .cursor/active-work-item.txt (legacy read only)
- If exists: type=work-item, id=content
- If not exists: prompt user to start a new Work Item
Parse content as `type:id`
Set root_path = work-items/{id}/
Set journal_path = journals/work-items/{id}/progress.md
```

## Example Usage

```
**Starting a new arrivals-day job:**
User: "start new work item WID-20261108"
Agent: writes `work-item:WID-20261108` to `.cursor/active-context.txt`
```

**Switching contexts:**

```
User: "switch to work item WID-654321"
Agent: reads current context (work-item:WID-123456)
writes new context (work-item:WID-654321)
confirms switch with user
```

## Benefits

- Single source of truth for active context
- One Work Item per stay date, reservation, group, or pack
- Easy to parse and validate
