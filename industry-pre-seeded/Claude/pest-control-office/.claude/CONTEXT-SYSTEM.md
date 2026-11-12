# Active Context System

## Purpose

Tracks which **Work Item** (route day, ticket pack, callback board, log pack, map set, WDO folder, or estimate) is active.

## Context File

- **Location:** `.claude/active-context.txt`
- **Format:** `<type>:<id>`
- **Examples:**
  - `work-item:WID-654321` (pest-office role job)

## Context Types

### work-item

- **Purpose:** One route day, one ticket pack, or one named pack (chemical-log completeness, bait-map index, WDO form, …)
- **ID Format:** `WID-XXXXXXXX`
- **Root Path:** `work-items/<id>/`
- **Journal:** `journals/work-items/<id>/progress.md`
- **Branch map:** `journals/work-items/<id>/state.json`
- **Node notes:** `journals/work-items/<id>/nodes/`
- **Workflows:** registered pest-office jobs in `.claude/workflows/workflow-registry.json`
- **Method:** `docs/role/work-item-method.md`

## Switching Context

User commands:
- `switch to work item WID-12345678` → writes `work-item:WID-12345678`

The agent will:
1. Parse the context file to determine type and ID
2. Route to `work-items/<id>/` and `journals/work-items/<id>/`
3. Load operations memory and the selected pest-office workflow

## Backward Compatibility

**Legacy file:** `.claude/active-work-item.txt` — read fallback only. Skills must not write it.

## Skill Integration

Skills that read context:
- **continue:** Reads context to determine next pest-office step
- **workflow-selector:** Writes context when starting new work
- **journal-keeper:** Reads context for journal path
- **switch-context:** Changes the active Work Item
- **remember / promote-facts-rules / operator-qa:** Use the active Work Item paths

All skills should:
1. Read `.claude/active-context.txt`
2. Parse format: `type:id`
3. Route based on type:
   - `work-item` → `work-items/<id>/` with journal under `journals/work-items/<id>/`

## Context Parsing Logic

```
Read .claude/active-context.txt
If file doesn't exist:
- Check .claude/active-work-item.txt (legacy read fallback)
- If exists: type=work-item, id=content
- If not exists: prompt user (workflow-selector) to start new work
Parse content as `type:id`
Set context_type = type (work-item)
Set context_id = id
Set root_path = work-items/{id}/
Set journal_path = journals/work-items/{id}/progress.md
Set map_path = journals/work-items/{id}/state.json
```

## Example Usage

```
**Starting new work item:**
User: "start Tuesday's route day"
Agent: workflow-selector → writes `work-item:WID-123456` to `.claude/active-context.txt`
```

**Switching contexts:**

```
User: "switch to work item WID-654321"
Agent: reads current context, writes new context, confirms switch
```

## Benefits

- Single source of truth for active context
- One route day / ticket / pack per Work Item
- Journals stay under `journals/work-items/<id>/`
