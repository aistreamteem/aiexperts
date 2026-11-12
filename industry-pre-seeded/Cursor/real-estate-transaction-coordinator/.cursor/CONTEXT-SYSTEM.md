# Active Context System

## Purpose

Tracks the transaction Work Item currently in progress.

## Context File

- **Location:** `.cursor/active-context.txt`
- **Format:** `<type>:<id>`
- **Example:** `work-item:WID-4412` or `work-item:2026-09-15-123-main-buy`

## Context Types

### work-item

- **Purpose:** One residential transaction file (dates calendar, missing docs, disclosures, closing pack, and related jobs)
- **ID Format:** `WID-XXXXXXXX` or a filesystem-safe pack name
- **Root Path:** `work-items/<id>/`
- **Folders:** `in/`, `work/`, `out/`, `evidence/`, `facts/`
- **Journal:** `journals/work-items/<id>/progress.md`, `state.json`, and `nodes/<active leaf>.md`
- **Workflows:** registered TC jobs in `.cursor/workflows/workflow-registry.json`

## Switching Context

User: `switch to work item WID-12345678` → writes `work-item:WID-12345678`

The agent:

1. Parses the context file
2. Routes to `work-items/<id>/`
3. Loads that journal, operations memory, and the selected workflow

## Backward Compatibility

**Legacy file:** `.cursor/active-work-item.txt` — read as a fallback only. Skills must not write it.

## Skill Integration

Skills that read context:

- **continue:** next ready workflow step
- **workflow-selector:** writes context when starting a pack
- **journal-keeper:** journal paths
- **switch-context:** changes the pointer
- **remember / promote-facts-rules / operator-qa:** Work Item vs expert memory

All skills should:

1. Read `.cursor/active-context.txt`
2. Parse `type:id`
3. Route `work-item` → `work-items/<id>/` for artifacts and `journals/work-items/<id>/` for journals

If the file is missing, check `.cursor/active-work-item.txt` (legacy); if that is missing, prompt for a Work Item / pack name.

## Example

Starting 123 Main St buy dates calendar: write `work-item:2026-09-15-123-main-buy`, copy `work-items/_TEMPLATE/`, run **workflow-selector** (default `dates-calendar`), put the executed contract PDF in `in/`.
