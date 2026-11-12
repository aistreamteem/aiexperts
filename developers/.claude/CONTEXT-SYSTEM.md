# Active Context System

## Purpose

Tracks which work item the user is currently working on, so every skill and hook reads and writes the same files.

## Context File

- **Location:** `.claude/active-context.txt`
- **Format:** `<type>:<id>`
- **Examples:**
  - `work-item:WID-654321` (development work)

## Context Types

### work-item

- **Purpose:** Development tasks (features, bugs, refactoring)
- **ID Format:** `WID-XXXXXXXX`
- **Root Path (artifacts):** `work-items/<id>/`
- **Journal:** `journals/work-items/<id>/progress.md` (item-wide fields), `journals/work-items/<id>/state.json` (branch map), `journals/work-items/<id>/nodes/<node>.md` (step notes, open questions, next action)
- **Workflows:** developer

## Switching Context

User commands:
- `switch to work item WID-12345678` → writes `work-item:WID-12345678`

The agent will:
1. Parse the context file to determine type and ID
2. Route to the artifact folder and the journal folder
3. Load the correct journal and artifacts

## Backward Compatibility

**Legacy file:** `.claude/active-work-item.txt`. It is no longer written. Skills and hooks may read it as a fallback when `active-context.txt` is missing.

## Skill Integration

Skills that read context:
- **continue:** reads context to determine next action
- **workflow-selector:** writes context when starting new work
- **switch-context:** writes context when the user switches
- **journal-keeper:** reads context for the journal paths
- **spec-parser:** reads context for artifact paths
- **hld-writer, dd-writer:** read context for artifact paths

All skills should:
1. Read `.claude/active-context.txt`
2. Parse format: `type:id`
3. Route based on type:
   - `work-item` → artifacts in `work-items/<id>/`, journal in `journals/work-items/<id>/`

## Context Parsing Logic

```
Read .claude/active-context.txt
If file doesn't exist:
- Check .claude/active-work-item.txt (legacy, read only)
- If exists: type=work-item, id=content
- If not exists: prompt user to start new work
Parse content as `type:id`
Set context_type = type (work-item)
Set context_id = id
Set root_path = work-items/{id}/
Set journal_dir = journals/work-items/{id}/
Set journal_path = {journal_dir}/progress.md
Set map_path = {journal_dir}/state.json
```

## Example Usage

**Starting new work item:**

```
User: "start new work item WID-123456"
Agent: writes `work-item:WID-123456` to `.claude/active-context.txt`
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
- Clear distinction between artifacts (`work-items/`) and journal (`journals/`)
- Support for multiple context types (extensible)
- Easy to parse and validate
