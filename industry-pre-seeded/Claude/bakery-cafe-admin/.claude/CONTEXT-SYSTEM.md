# Active Context System

## Purpose

Tracks the active **Work Item** for this bakery / cafe production office (bake date, wholesale day, cake board, receiving ticket, holiday pack).

## Context File

- **Location:** `.claude/active-context.txt`
- **Format:** `<type>:<id>`
- **Examples:**
  - `work-item:WID-654321`
  - `work-item:2026-11-08-bake-list`

## Context Types

### work-item

- **Purpose:** One bakery-cafe job pack
- **ID Format:** `WID-XXXXXXXX` or a pack name (`YYYY-MM-DD-bake-list`)
- **Root Path:** `work-items/<id>/`
- **Journal:** `journals/work-items/<id>/progress.md`
- **Workflows:** registered jobs in `.claude/workflows/workflow-registry.json` (default `bake-list-day`)
- **Method:** `docs/role/work-item-method.md`

## Switching Context

User commands:

- `switch to work item WID-12345678`
- `switch to 2026-11-08-bake-list`

The agent will:

1. Parse the context file
2. Route to `work-items/<id>/`
3. Load that Work Item journal and artifacts

## Backward Compatibility

**Legacy file:** `.claude/active-work-item.txt` (read-only fallback). Do not write it.

## Skill Integration

Skills that read context:

- **continue** — next ready step of the selected job
- **workflow-selector** — writes context when starting new work
- **journal-keeper** — journal path
- **switch-context** — changes the pointer

All skills should:

1. Read `.claude/active-context.txt`
2. Parse `type:id`
3. Route `work-item` → `work-items/<id>/`
4. Use `journals/work-items/<id>/progress.md` as the flat journal and `nodes/<active leaf>.md` for step notes

## Context Parsing Logic

```
Read .claude/active-context.txt
If file doesn't exist:
- Check .claude/active-work-item.txt (legacy, read-only)
- If exists: type=work-item, id=content
- If not exists: prompt to start a Work Item (workflow-selector)
Parse content as `type:id`
Set root_path = work-items/{id}/
Set journal_path = journals/work-items/{id}/progress.md
```

## Example Usage

**Starting a Tuesday bake list:**

```
User: "start work item 2026-11-08-bake-list"
Agent: writes `work-item:2026-11-08-bake-list` to `.claude/active-context.txt`
```

**Switching:**

```
User: "switch to work item 2026-11-09-wholesale"
Agent: writes new context, confirms the journal next action
```
