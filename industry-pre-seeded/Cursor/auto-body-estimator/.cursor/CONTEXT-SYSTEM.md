# Active Context System

## Purpose

Tracks which **Work Item** (assignment / RO / claim pack) is active for this Auto body estimator / office Expert.

## Context File

- **Location:** `.cursor/active-context.txt`
- **Format:** `<type>:<id>`
- **Examples:**
  - `work-item:WID-654321`
  - `work-item:2026-09-15-ro-2104`

## Context Types

### work-item

- **Purpose:** One collision-shop office job (intake, estimate pack, photo index, supplement, and related phases in `docs/role/work-item-method.md`)
- **ID Format:** `WID-XXXXXXXX` or a shop-style folder name (`YYYY-MM-DD-ro-or-claim`)
- **Root Path:** `work-items/<id>/`
- **Journal:** `journals/work-items/<id>/progress.md`
- **State:** `journals/work-items/<id>/state.json`
- **Workflows:** registered jobs in `.cursor/workflows/workflow-registry.json` (default `assignment-intake`)

## Switching Context

User commands:
- `switch to work item WID-12345678` → writes `work-item:WID-12345678`

The agent will:
1. Parse the context file to determine type and ID
2. Route to `work-items/<id>/`
3. Load the Work Item journal, shared memory, and that item’s facts/rules

## Backward Compatibility

**Legacy file:** `.cursor/active-work-item.txt`

## Skill Integration

Skills that read context:
- **continue:** Reads context to determine next workflow step
- **workflow-selector:** Writes context when starting new work
- **journal-keeper:** Reads context for journal path
- **switch-context:** Changes the active Work Item
- **remember:** Routes Work Item vs Expert Role memory

All skills should:
1. Read `.cursor/active-context.txt`
2. Parse format: `type:id`
3. Route `work-item` → `work-items/<id>/`

## Context Parsing Logic

```
Read .cursor/active-context.txt
If file doesn't exist:
- Check .cursor/active-work-item.txt (legacy)
- If exists: type=work-item, id=content
- If not exists: prompt user to start a Work Item (assignment / RO / claim)
Parse content as `type:id`
Set root_path = work-items/{id}/
Set journal_path = journals/work-items/{id}/progress.md
```

## Example Usage

```
**Starting new work item:**
User: "start new work item 2026-09-15-ro-2104"
Agent: writes `work-item:2026-09-15-ro-2104` to `.cursor/active-context.txt`
```

**Switching contexts:**

```
User: "switch to work item WID-654321"
Agent: reads current context, writes the new id, confirms
```

## Benefits

- One assignment per folder
- Journals stay under `journals/` (not a top-level role state file named journal)
- Registered workflows, not a developer HLD/DD path
