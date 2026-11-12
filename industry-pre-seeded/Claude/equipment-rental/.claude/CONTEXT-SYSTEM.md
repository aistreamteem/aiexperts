# Active Context System

## Purpose

Tracks the active **Work Item** for this equipment-rental role (one contract, reservation day, delivery run, inspection pack, or similar).

## Context File

- **Location:** `.claude/active-context.txt`
- **Format:** `<type>:<id>`
- **Examples:**
  - `work-item:WID-654321`
  - `work-item:2026-11-08-contract-331`

## Context Types

### work-item

- **Purpose:** One rental-role job using `docs/role/work-item-method.md`
- **ID Format:** `WID-XXXXXXXX` or a filesystem-safe job name
- **Root Path:** `work-items/<id>/`
- **Journal:** `journals/work-items/<id>/progress.md`
- **Branch map:** `journals/work-items/<id>/state.json`
- **Node notes:** `journals/work-items/<id>/nodes/<leaf>.md`
- **Workflows:** registered jobs in `.claude/workflows/workflow-registry.json` (default `contract-completeness`)

The legacy work-item pointer journal under the artifact folder is removed from the template. Write only under `journals/work-items/<id>/`.

## Switching Context

User commands:

- `switch to work item WID-12345678` → writes `work-item:WID-12345678`

The agent will:

1. Parse the context file to determine type and ID
2. Route to `work-items/<id>/`
3. Load that Work Item journal, facts, and artifacts

## Backward Compatibility

**Legacy file:** `.claude/active-work-item.txt` — read-only fallback for old copies. Skills and hooks must not write it.

## Skill Integration

Skills that read context: **continue**, **workflow-selector**, **journal-keeper**, **remember**, **switch-context**, **operator-qa**, **promote-facts-rules**.

All skills should:

1. Read `.claude/active-context.txt`
2. Parse `type:id`
3. Route `work-item` → `work-items/<id>/` and `journals/work-items/<id>/`

## Context Parsing Logic

```
Read .claude/active-context.txt
If file doesn't exist:
- Check .claude/active-work-item.txt (legacy, read only)
- If exists: type=work-item, id=content
- If not exists: prompt user to start a Work Item
Parse content as `type:id`
Set root_path = work-items/{id}/
Set journal_path = journals/work-items/{id}/progress.md
Set map_path = journals/work-items/{id}/state.json
```

## Example Usage

**Starting a new work item:**

```
User: "start new work item WID-123456"
Agent: writes `work-item:WID-123456` to `.claude/active-context.txt`
```

**Switching contexts:**

```
User: "switch to work item WID-654321"
Agent: reads current context, writes the new one, confirms
```
