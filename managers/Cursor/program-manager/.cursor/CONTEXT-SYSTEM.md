# Active context

`.cursor/active-context.txt` stores `<type>:<id>`. Today the type is `work-item`.

| Type | Example | Purpose |
| --- | --- | --- |
| work-item | `work-item:WID-21411151` | Management work for this Program Manager expert: planned initiatives and escalations |

Older checkouts may still have `.cursor/active-work-item.txt`. Hooks and continue may read it as a fallback. Do not write it.

| What | Where |
| --- | --- |
| Expert journal | `journals/expert/progress.md` |
| Work-item journal | `journals/work-items/<id>/progress.md` |
| Branch map | `journals/work-items/<id>/state.json` |
| Step notes | `journals/work-items/<id>/nodes/` |
| Agent notes | `journals/work-items/<id>/agent-notes/` |
| Artifacts | `work-items/<id>/` |

Workflows for a work item: `program-delivery`, `program-escalation`.

Role onboarding is not a work item. It writes `docs/role/role-definition.md` and updates `MyRole.txt`.
