# Active Context System

## Purpose

Tracks whether the user is currently working on a **Work Item** (a fleet dispatch pack: assignment, routes, DVIR, exceptions, POD, or file questions).

## Context File

- **Location:** `.claude/active-context.txt`
- **Format:** `<type>:<id>`
- **Examples:**
  - `work-item:WID-654321`
  - `work-item:2026-09-15-truck-14-route-a`

## Context Types

### work-item

- **Purpose:** One dispatch pack (one service date, unit, or named board)
- **ID Format:** `WID-XXXXXXXX` or a dated pack name
- **Root Path:** `work-items/<id>/`
- **Journal:** `journals/work-items/<id>/progress.md`, `state.json`, and `nodes/` (do not write under `work-items/<id>/journal/`)
- **Workflows:** registered jobs in `.claude/workflows/workflow-registry.json` (default `assignment-pack`)
- **Method:** `docs/role/work-item-method.md`

## Switching Context

User commands:
- `switch to work item WID-12345678` → writes `work-item:WID-12345678`

The agent will:
1. Parse the context file to determine type and ID
2. Route to `work-items/<id>/`
3. Load the Work Item journal and artifacts

## Backward Compatibility

**Legacy file:** `.claude/active-work-item.txt` — **read-only fallback**. Skills must not write it.

## Skill Integration

Skills that read context:
- **continue:** Reads context to determine next action
- **workflow-selector:** Writes context when starting new work
- **journal-keeper:** Reads context for journal path
- **switch-context:** Changes the active id
- **remember / operator-qa / promote-facts-rules:** Scope facts and Q&A to the active Work Item

All skills should:
1. Read `.claude/active-context.txt`
2. Parse format: `type:id`
3. Route based on type:
   - `work-item` → `work-items/<id>/` artifacts and `journals/work-items/<id>/` journal

## Context Parsing Logic

```
Read .claude/active-context.txt
If file doesn't exist:
- Check .claude/active-work-item.txt (legacy, read-only)
- If exists: type=work-item, id=content
- If not exists: prompt user to start new work
Parse content as `type:id`
Set context_type = type (work-item)
Set context_id = id
Set root_path = work-items/{id}/
Set journal_path = journals/work-items/{id}/progress.md
```

## Example Usage

```
**Starting new work item:**
User: "start today's routes for 2026-09-15 truck 14"
Agent: writes `work-item:2026-09-15-truck-14-route-a` to `.claude/active-context.txt`
```

**Switching contexts:**

```
User: "switch to work item WID-654321"
Agent: reads current context (work-item:2026-09-15-truck-14-route-a)
writes new context (work-item:WID-654321)
confirms switch with user
```

## Benefits

- Single source of truth for active context
- One pack per Work Item so service dates do not mix
- Easy to parse and validate
