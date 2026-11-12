# Active Context System

## Purpose

Tracks the active **Work Item** for this Auto shop service advisor role (one RO pack, board list, MPI, estimate, auth gap, findings, parts, comeback, or pickup).

## Context File

- **Location:** `.cursor/active-context.txt`
- **Format:** `<type>:<id>`
- **Examples:**
  - `work-item:WID-654321` (RO / pack work)
  - `work-item:2026-09-15-ro-5521`

## Context Types

### work-item

- **Purpose:** One repair order, board export, or related pack for this role
- **ID Format:** `WID-XXXXXXXX` or a shop-readable id (`YYYY-MM-DD-ro-5521`)
- **Root Path:** `work-items/<id>/`
- **Journal:** `journals/work-items/<id>/progress.md`, `state.json`, and `nodes/`
- **Workflows:** registered role jobs in `.cursor/workflows/workflow-registry.json` (default `one-ro`)
- **Method:** `docs/role/work-item-method.md`

## Switching Context

User commands:
- `switch to work item WID-12345678` → writes `work-item:WID-12345678`

The agent will:
1. Parse the context file to determine type and ID
2. Route to `work-items/<id>/`
3. Load the Work Item journal, operations memory, and artifacts under `in/`, `work/`, `out/`, `evidence/`

## Backward Compatibility

**Legacy file:** `.cursor/active-work-item.txt` — read as a fallback only. Skills must not write it.

## Skill Integration

Skills that read context:
- **continue:** Reads context to determine next workflow step
- **workflow-selector:** Writes context when starting new work
- **journal-keeper:** Reads context for journal path
- **switch-context:** Changes the active Work Item
- **remember / promote-facts-rules / operator-qa:** Use the active Work Item for WI-scoped memory and Q&A

All skills should:
1. Read `.cursor/active-context.txt`
2. Parse format: `type:id`
3. Route based on type:
   - `work-item` → `work-items/<id>/`

## Context Parsing Logic

```
Read .cursor/active-context.txt
If file doesn't exist:
- Check .cursor/active-work-item.txt (legacy read fallback)
- If exists: type=work-item, id=content
- If not exists: prompt user to start a Work Item (workflow-selector)
Parse content as `type:id`
Set context_type = type (work-item)
Set context_id = id
Set root_path = work-items/{id}/
Set journal_path = journals/work-items/{id}/progress.md
```

## Example Usage

```
**Starting new work item:**
User: "start new work item for RO 5521"
Agent: writes `work-item:2026-09-15-ro-5521` (or WID-…) to `.cursor/active-context.txt`
Selects workflow `one-ro` unless the operator names another registered job
```

**Switching contexts:**

```
User: "switch to work item WID-654321"
Agent: reads current context, writes new context, confirms switch
```

## Benefits

- Single source of truth for the active RO pack
- Isolation between tickets
- Easy to parse and validate
