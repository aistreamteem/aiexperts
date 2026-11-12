# How Memory Loading Works

This janitorial-office expert loads **shared** memory (all jobs) plus **operations** memory, then filters by the selected role job.

## Discovery

1. Load `facts/MEMORY-INDEX.md`.
2. Read `.cursor/active-context.txt` (`work-item:<id>`; legacy fallback `.cursor/active-work-item.txt`).
3. Load:

```text
1. facts-shared.md + rules-shared.md
2. facts-operations.md + rules-operations.md
3. work-items/<id>/facts/facts.md + rules.md when present
```

4. Include Expert Role entries whose `**Workflows:**` is `all` or matches the current role job.
5. Load only the tool doc named by the current workflow step under `docs/tools/`.

## Routing

- `Workflows: all` → shared pair
- Job-scoped entries → operations pair
- Pack-only notes → Work Item `facts/`

Do **not** default to a software-build or incident-response pipeline.

## Maintenance

- Health check: `py -3 .cursor/skills/memory-optimize/scripts/analyze-memory.py facts`
- Warning if a memory file exceeds ~1,500 lines
- Update MEMORY-INDEX when a new topic appears
- After retagging rules: `python scripts/memory/build_trigger_index.py`
