# Active Context System

## Purpose

Tracks which **Work Item** (crew day, ticket, week, pack) this landscaping / lawn-care office Expert is on.

## Context File

- **Location:** `.claude/active-context.txt`
- **Format:** `<type>:<id>`
- **Examples:**
  - `work-item:WID-654321`
  - `work-item:2026-09-15-crew-a`

## Context Types

### work-item

- **Purpose:** One role job (route pack, crew day, estimate, material pull, callback list, …)
- **ID Format:** `WID-XXXXXXXX` or a shop-style folder name (`YYYY-MM-DD-property-or-crew`)
- **Root Path:** `work-items/<id>/`
- **Journal:** `journals/work-items/<id>/progress.md` (flat), `state.json`, and `nodes/<leaf>.md`
- **Workflows:** registered role jobs in `.claude/workflows/workflow-registry.json` (see `docs/role/work-item-method.md`)

## Switching Context

User commands:

- `switch to work item WID-12345678`
- `switch to 2026-09-15-crew-a`

The agent will:

1. Parse the context file
2. Route to `work-items/<id>/`
3. Load that Work Item journal, STATUS, and facts/rules

## Backward Compatibility

**Legacy file:** `.claude/active-work-item.txt` — read fallback only. Do not write it.

## Skill Integration

Skills that read context: **continue**, **workflow-selector**, **journal-keeper**, **remember**, **switch-context**, **operator-qa**.

All skills should:

1. Read `.claude/active-context.txt`
2. Parse `type:id`
3. Route `work-item` → `work-items/<id>/` and `journals/work-items/<id>/`

## Context Parsing Logic

```
Read .claude/active-context.txt
If missing:
  Check .claude/active-work-item.txt (legacy read only)
  If exists: type=work-item, id=content
  If not: prompt for a job id (crew day, ticket, week)
Parse `type:id`
root_path = work-items/{id}/
journal_path = journals/work-items/{id}/progress.md
```

## Example

Starting a crew day: operator says the date and crew → write `work-item:2026-09-15-crew-a` → **workflow-selector** picks `crew-day` → **continue** walks the first ready step.
