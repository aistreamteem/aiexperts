# Context System

Tracks which **Work Item** (service date, vendor truck, shift prep, invoice, catering event, or waste recap) is active.

## Active context file

**File:** `.cursor/active-context.txt`

- One line: `work-item:<id>`
- Examples:
  - `work-item:WID-654321`
  - `work-item:2026-11-08-dinner-prep`

**Legacy read fallback:** `.cursor/active-work-item.txt` (do not write this file).

## Work Item layout

- **Purpose:** One pack or named kitchen job
- **Artifacts:** `work-items/<id>/` with `in/`, `work/`, `out/`, `evidence/`
- **Journal:** `journals/work-items/<id>/progress.md` (item-wide fields)
- **Branch map:** `journals/work-items/<id>/state.json`
- **Node notes:** `journals/work-items/<id>/nodes/<node>.md`
- **Agent notes:** `journals/work-items/<id>/agent-notes/`
- **Workflows:** registered kitchen jobs in `.cursor/workflows/workflow-registry.json`

## Expert journal

`journals/expert/progress.md` holds the current work item line and future work.

## Loading order

1. Read `.cursor/active-context.txt` (legacy fallback if missing)
2. Read expert journal, then Work Item flat journal and active nodes
3. Load operations memory and the selected kitchen workflow
4. Use `journals/work-items/<id>/progress.md` as the flat journal

## Skills that touch context

- **continue:** Reads context to determine next kitchen-job step
- **workflow-selector:** Writes `active-context.txt` when starting a job
- **switch-context:** Rewrites `active-context.txt` only
- **journal-keeper:** Updates expert and Work Item journals under `journals/`
- **remember / promote-facts-rules:** Use the active Work Item id from context

## Parsing logic

```
active-context.txt → work-item:<id>
  → work-items/<id>/          (artifacts)
  → journals/work-items/<id>/ (progress.md, state.json, nodes/)
```

If `active-context.txt` is missing:

- Check `.cursor/active-work-item.txt` (legacy)
- Else read `Current work item:` from `journals/expert/progress.md`
- Else ask via workflow-selector / continue

## Example

User: "start dinner prep for 2026-11-08"

1. Write `.cursor/active-context.txt` → `work-item:2026-11-08-dinner-prep`
2. Ensure `work-items/2026-11-08-dinner-prep/` and `journals/work-items/2026-11-08-dinner-prep/`
3. Select `prep` (or ask) and set next action from that workflow file
