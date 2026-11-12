# How Memory Loading Works

This Auto body estimator / office Expert loads **shared** Expert Role memory for every Work Item, then that claim’s Work Item facts/rules.

## Discovery

1. Always load `facts/MEMORY-INDEX.md` first.
2. Read `.cursor/active-context.txt` (legacy fallback: `.cursor/active-work-item.txt`).
3. Load `facts/facts-shared.md` and `facts/rules-shared.md`.
4. When a Work Item is active, also load `work-items/<id>/facts/facts.md` and `rules.md` when present.
5. Load a `docs/tools/` file only when the current YAML step cites it.

## Routing

| Session | Memory |
| --- | --- |
| Work Item under `work-items/<id>/` | shared pair + Work Item `facts/` |
| No Work Item yet | shared pair only |

`Workflows: all` entries live in the shared pair so every registered job’s loader includes them. This seed does not use a separate developer or incident-response memory pair.

## Maintenance

Run `py -3 .cursor/skills/memory-optimize/scripts/analyze-memory.py facts` against the shared pair. Missing coding-pipeline memory files is not an error on this role.
