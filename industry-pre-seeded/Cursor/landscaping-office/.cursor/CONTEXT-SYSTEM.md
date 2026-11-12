# Active Context System

## Purpose

Tracks the active **Work Item** (landscaping-office pack: crew day, route, estimate, material pull, weather postpone, callback, photo pack, seasonal calendar, enhancement ticket).

## Context File

- **Location:** `.cursor/active-context.txt`
- **Format:** `<type>:<id>`
- **Example:** `work-item:WID-654321` or `work-item:2026-09-15-crew-a`

## Context Types

### work-item

- **Purpose:** One job pack (one crew day, property + date, ticket, or week)
- **ID Format:** `WID-XXXXXXXX` or a shop pack id they named
- **Root Path:** `work-items/<id>/`
- **Folders:** `in/`, `work/`, `out/`, `evidence/`
- **Journal:** `journals/work-items/<id>/progress.md`
- **Branch map:** `journals/work-items/<id>/state.json`
- **Node notes:** `journals/work-items/<id>/nodes/`
- **Agent notes:** `journals/work-items/<id>/agent-notes/`
- **Workflows:** registry jobs in `.cursor/workflows/workflow-registry.json`

Method: `docs/role/work-item-method.md`.

## Switching Context

User: `switch to work item WID-12345678` → writes `work-item:WID-12345678`

The agent:

1. Parse the context file
2. Route to `work-items/<id>/`
3. Load that journal, operations memory, and the selected job instruction file

## Backward Compatibility

**Legacy file:** `.cursor/active-work-item.txt` — read fallback only. Do not write it.

## Skill Integration

Skills that read context: **continue**, **workflow-selector**, **journal-keeper**, **switch-context**, **remember**, **promote-facts-rules**, **operator-qa**.

All of them:

1. Read `.cursor/active-context.txt`
2. Parse `type:id`
3. Route `work-item` → `work-items/<id>/` for artifacts and `journals/work-items/<id>/` for journals

## Context Parsing Logic

```
Read .cursor/active-context.txt
If missing:
  Check .cursor/active-work-item.txt (legacy read fallback)
  If exists: type=work-item, id=content
  Else: prompt for a Work Item / crew day / ticket / week
Parse type:id
root_path = work-items/<id>/
journal_path = journals/work-items/<id>/progress.md
node_notes = journals/work-items/<id>/nodes/
```
