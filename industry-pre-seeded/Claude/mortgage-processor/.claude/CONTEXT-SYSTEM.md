# Active Context System

## Purpose

Tracks the processor Work Item (loan or pack) currently in progress.

## Context File

- **Location:** `.claude/active-context.txt`
- **Format:** `<type>:<id>`
- **Example:** `work-item:WID-4412` or `work-item:2026-09-15-loan-4412`

## Context Types

### work-item

- **Purpose:** One loan file pack (conditions, missing docs, dates, third-party index)
- **ID Format:** `WID-XXXXXXXX` or a filesystem-safe pack name
- **Root Path:** `work-items/<id>/`
- **Folders:** `in/`, `work/`, `out/`, `evidence/`, `facts/`
- **Journal:** `journals/work-items/<id>/progress.md`, `state.json`, and `nodes/<active leaf>.md`
- **Workflows:** registered processor jobs in `.claude/workflows/workflow-registry.json`

## Switching Context

User: `switch to work item WID-12345678` → writes `work-item:WID-12345678`

The agent:

1. Parses the context file
2. Routes to `work-items/<id>/`
3. Loads that journal, shared memory, and the selected workflow

## Backward Compatibility

**Legacy file:** `.claude/active-work-item.txt` — read as a fallback only. Skills must not write it.

## Skill Integration

Skills that read context:

- **continue:** next ready workflow step
- **workflow-selector:** writes context when starting a pack
- **journal-keeper:** journal paths
- **switch-context:** changes the pointer
- **remember / promote-facts-rules / operator-qa:** Work Item vs expert memory

All skills should:

1. Read `.claude/active-context.txt`
2. Parse `type:id`
3. Route `work-item` → `work-items/<id>/` for artifacts and `journals/work-items/<id>/` for journals

If the file is missing, check `.claude/active-work-item.txt` (legacy); if that is missing, prompt for a Work Item / pack name.

## Example

Starting loan 4412 conditions: write `work-item:2026-09-15-loan-4412`, copy `work-items/_TEMPLATE/`, run **workflow-selector** (default `conditions-checklist`), put the LOS export in `in/`.
