# Expert — skill design

**Updated:** 2026-11-08  
**Folder:** Landscaping / lawn-care office Expert.

This Expert uses the **canonical expert skills** plus **role workflows** for a US lawn-care / landscape-maintenance office. Software-build pipelines are not part of this role. **continue**, **journal-keeper**, registered workflow files, and Work Item folders cover the role loop. Canonical platform skills from the base expert (including pipeline skills) are kept.

Use ordinary words with the person. Finished work is a **pack in `work-items/<id>/out/`** plus a journal / STATUS note. Look in saved files before starting. Do not invent missing tickets, prices, weather calls, mixes, or wages.

Work-item method: `docs/role/work-item-method.md`.

## Canonical expert skills (keep)

| Skill | Role |
| --- | --- |
| **continue** | Resume from `journals/expert/progress.md` + active Work Item journal. One ready workflow step. Continue is not a yes. |
| **define-role** | First session if Role status is pending; write `MyRole.txt` and stub workflows. |
| **journal-keeper** | Update expert and Work Item journals after steps, answers, failures. |
| **remember** | Save facts/rules into shared memory or Work Item `facts/`. |
| **workflow-selector** | Pick a registered role job from `workflow-registry.json`. |
| **operator-qa** | Clarify missing shop knowledge before acting. |
| **promote-facts-rules** | Elevate Work Item learnings into `facts-shared` / `rules-shared`. |
| **switch-context** | Change the active Work Item. |
| **integrate-docs** | Fold dropped notes/packets into shared memory. |
| **memory-optimize** | Health-check shared memory files. |
| **visual-page** | Optional shared visual when a picture of the route, day list, or calendar helps. |
| **spec-parser** | Parse a requirements/spec into the Work Item journal when that workflow applies. |
| **scaffold-project** | Create the project skeleton after approved design when scaffolding applies. |
| **implement-feature** | Implement one TODOS task when the journal next action calls for it. |
| **iterative-feature** | Requirements → design → implement → test for iterative changes. |
| **refactor** | Reduce duplication / tech debt while keeping tests green. |
| **diagram-generator** | Regenerate or sync design diagrams with design docs when needed. |

## Role workflows (not skills)

Named jobs live under `.claude/workflows/` and are listed in `workflow-registry.json`: callback-list, crew-day, enhancement-ticket, estimate-from-price, material-pull, photo-pack, route-pack, seasonal-calendar, weather-postpone-list.

Each file is self-contained: steps, needs, produces, tool doc, check. **continue** walks those steps. Tools live under `docs/tools/`.

## Memory

- `facts/MEMORY-INDEX.md` — load first
- `facts/facts-shared.md` / `facts/rules-shared.md` — this role’s knowledge
- `work-items/<id>/facts/` — this job only
- `journals/expert/progress.md` + `journals/work-items/<id>/` — live state
