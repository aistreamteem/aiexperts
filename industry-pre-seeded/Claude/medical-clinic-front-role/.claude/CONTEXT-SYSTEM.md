# Context System

How this medical clinic front role Expert tracks the active Work Item and journals.

## Active context

**Current pointer:** `.claude/active-context.txt`  
One line: `work-item:<id>`

**Legacy file (read fallback only):** `.claude/active-work-item.txt`  
Do not write this file. Older copies may still be read by continue and hooks.

## Journals

| What | Where |
| --- | --- |
| Expert journal | `journals/expert/progress.md` |
| Work-item journal (item-wide fields) | `journals/work-items/<id>/progress.md` |
| Branch map | `journals/work-items/<id>/state.json` |
| Step notes, open questions, next action | `journals/work-items/<id>/nodes/<node>.md` |
| Background-agent notes | `journals/work-items/<id>/agent-notes/` |
| Artifacts (pack, STATUS, facts) | `work-items/<id>/` |

Skills that write progress use **journal-keeper**. Hooks read `.claude/active-context.txt`, then the legacy pointer, then the expert journal **Current work item** line.

## Parsing

1. Read `.claude/active-context.txt` → `work-item:<id>`
2. Else read `.claude/active-work-item.txt` (legacy)
3. Else read `journals/expert/progress.md` for **Current work item**
4. Load `journals/work-items/<id>/progress.md` and the active leaf from `state.json`

There is no `work-items/<id>/journal/progress.md` write path.
