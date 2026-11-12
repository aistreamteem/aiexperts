# Active Context System

## Purpose

Tracks which **production-scheduler pack** (Work Item) is active.

## Context File

- **Location:** `.cursor/active-context.txt`
- **Format:** `<type>:<id>`
- **Examples:**
  - `work-item:WID-654321`
  - `work-item:2026-11-08-dispatch`

## Context Types

### work-item

- **Purpose:** One shop pack (dispatch board, kit/shortage list, traveler completeness, WIP, due-date, outside-process, machine-down, pending ECO)
- **ID Format:** `WID-XXXXXXXX` or a dated pack name
- **Root Path:** `work-items/<id>/`
- **Journal:** `journals/work-items/<id>/progress.md`
- **Branch map:** `journals/work-items/<id>/state.json`
- **Node notes:** `journals/work-items/<id>/nodes/`
- **Workflows:** registered jobs in `.cursor/workflows/workflow-registry.json` (default `dispatch-list`)
- **Method:** `docs/role/work-item-method.md`

## Switching Context

User commands:
- `switch to work item WID-12345678` → writes `work-item:WID-12345678`
- `switch to 2026-11-08-dispatch` → writes `work-item:2026-11-08-dispatch`

The agent will:
1. Parse the context file to determine type and ID
2. Route to `work-items/<id>/` and `journals/work-items/<id>/`
3. Load that pack’s journal, STATUS, and selected workflow file

## Backward Compatibility

**Legacy file:** `.cursor/active-work-item.txt` — read fallback only. New writes go only to `.cursor/active-context.txt`.

## Skill Integration

Skills that read context:
- **continue:** Reads context to determine next action
- **workflow-selector:** Writes context when starting a new pack
- **journal-keeper:** Reads context for journal path
- **switch-context:** Changes the active Work Item
- **remember / promote-facts-rules:** Route memory using the active Work Item

All skills should:
1. Read `.cursor/active-context.txt`
2. Parse format: `type:id`
3. Route `work-item` → `work-items/<id>/` and `journals/work-items/<id>/`

## Context Parsing Logic

```
Read .cursor/active-context.txt
If file doesn't exist:
- Check .cursor/active-work-item.txt (legacy read fallback)
- If exists: type=work-item, id=content
- If not exists: prompt user to start a pack (workflow-selector)
Parse content as `type:id`
Set root_path = work-items/{id}/
Set journal_path = journals/work-items/{id}/progress.md
```

## Benefits

- Single source of truth for the active pack
- Day boards, WO packets, and shortage lists stay in separate folders
- Easy to parse and validate
