# Active Context System

## Purpose

Tracks whether the operator is currently working on an HOA / association admin Work Item (ACC packet, dues aging, board files, violations, and the other registered jobs).

How a Work Item runs: `docs/role/work-item-method.md`.

## Context File

- **Location:** `.claude/active-context.txt`
- **Format:** `<type>:<id>`
- **Examples:**
  - `work-item:WID-654321` (this week's ACC completeness pack)

## Context Types

### work-item

- **Purpose:** One association job: a meeting, application, aging as-of date, bid project, vendor certificate batch, work-order list, election tally, or reserve-study index
- **ID Format:** `WID-XXXXXXXX`
- **Root Path:** `work-items/<id>/`
- **Journal:** `journals/work-items/<id>/progress.md` (item-wide fields), `state.json` (branch map), `nodes/<leaf>.md` (step notes)
- **Workflows:** keys in `.claude/workflows/workflow-registry.json`

## Switching Context

Operator commands:

- `switch to work item WID-12345678` → writes `work-item:WID-12345678`

The agent will:

1. Parse the context file to determine type and ID
2. Route to `work-items/<id>/`
3. Load the correct journal, operations memory, and registered workflow

## Backward Compatibility

**Legacy read-only fallback:** `.claude/active-work-item.txt` (do not write this file; hooks and continue may still read it on old copies)

## Skill Integration

Skills that read context:

- **continue:** Reads context to determine next action
- **workflow-selector:** Writes context when starting new work
- **journal-keeper:** Reads context for journal path
- **switch-context:** Changes the active Work Item
- **remember / promote-facts-rules / operator-qa:** Use the active Work Item paths

All skills should:

1. Read `.claude/active-context.txt`
2. Parse format: `type:id`
3. Route based on type:
   - `work-item` → `work-items/<id>/`

## Context Parsing Logic

```
Read .claude/active-context.txt
If file doesn't exist:
- Check .claude/active-work-item.txt (legacy)
- If exists: type=work-item, id=content
- If not exists: prompt to start a new Work Item (workflow-selector)
Parse content as `type:id`
Set context_type = type (work-item)
Set context_id = id
Set root_path = work-items/{id}/
Set journal_path = journals/work-items/{id}/progress.md
```

## Example Usage

```
**Starting a new work item:**
Operator: "start new work item for June board files"
Agent: writes `work-item:WID-…` to `.claude/active-context.txt`, offers registered jobs from the registry
```

**Switching contexts:**

```
Operator: "switch to work item WID-654321"
Agent: reads current context, confirms, writes new context, reads that Work Item journal
```
