# How Memory Loading Works

## Short answer

This optometry front-role Expert loads **operations** memory for every Work Item. There is no developer or production-incident default.

## Discovery

### Step 1: Navigation index (always first)

Read `facts/MEMORY-INDEX.md`.

### Step 2: Active Work Item

1. Read `.cursor/active-context.txt` (legacy read fallback: `.cursor/active-work-item.txt`)
2. Resolve `work-items/<id>/` and `journals/work-items/<id>/`
3. Never default to `developer` or `production-incident`

### Step 3: Load operations files only

1. `facts/MEMORY-INDEX.md`
2. `facts/facts-operations.md` + `facts/rules-operations.md`
3. `work-items/<id>/facts/facts.md` + `rules.md` when present
4. Filter Expert Role entries by `**Workflows:**` (`all` or the current job id)

### Step 4: On-demand tools and lists

Load the `docs/tools/` file named by the active workflow step. Action-time rules also arrive via `.cursor/hooks/inject_rules_on_action.py` using `facts/trigger-index.json`.

## Routing

| Capture | Destination |
| --- | --- |
| Expert Role fact/rule (`Workflows: all` or a job id) | `facts/facts-operations.md` / `facts/rules-operations.md` |
| Work Item only | `work-items/<id>/facts/` |
| Tool / export how-to | `docs/tools/` |

## Configuration

See `AGENTS.md` rules on remember, facts/rules discipline, and Work Item isolation.

## Quarterly health check

Run `py -3 .cursor/skills/memory-optimize/scripts/analyze-memory.py facts`.
