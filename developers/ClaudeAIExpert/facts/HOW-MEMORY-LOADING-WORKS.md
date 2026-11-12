# How Memory Loading Works

The agent cannot load every memory file on every turn. It loads a small, fixed set by workflow, and surfaces individual rules at the moment they matter.

## Files

| Scope | Files |
| --- | --- |
| Shared (every workflow) | `facts/facts-shared.md`, `facts/rules-shared.md` |
| Workflow pair | `facts/facts-developer.md` / `facts/rules-developer.md`, or `facts/facts-incident-response.md` / `facts/rules-incident-response.md` |
| Work item | `work-items/<id>/facts/facts.md`, `work-items/<id>/facts/rules.md` |
| Index | `facts/MEMORY-INDEX.md` (entry formats, navigation) |
| Trigger index | `facts/trigger-index.json` and `facts/TRIGGER-INDEX.md` (generated) |

## Session-start loading (workflow axis)

Skills such as `continue`, `spec-parser`, `implement-feature`, and `iterative-feature` load memory in this order:

1. `facts/MEMORY-INDEX.md`
2. The shared pair
3. The pair for the work item's `Workflow type` (from `journals/work-items/<id>/progress.md`)
4. The work item pair, unfiltered

Each expert entry has a `**Workflows:**` field (default `all`). An entry is kept when the field is `all` or names the current workflow. Entries marked `all` live in the shared pair, so every workflow loads them. Rules MUST be followed; facts give context. Violations are logged to the journal.

## Action-time surfacing (trigger axis)

Some rules matter only at a particular action, whatever the workflow.

1. A rule carries `**Triggers:**` with tokens such as `write:sql`, `write:doc`, `pr:open`, `git:push`, `git:commit`.
2. `python scripts/memory/build_trigger_index.py` scans every `facts/rules-*.md` and writes `trigger-index.json` and `TRIGGER-INDEX.md`. It warns about rules with no `Triggers:` line and about tokens the hook cannot produce.
3. The PreToolUse hook `.claude/hooks/inject_rules_on_action.py` runs before every tool call. It classifies the pending action into tokens, looks them up in `trigger-index.json`, and injects the full text of each matching rule.

The token vocabulary is the `KNOWN_TOKENS` table in the hook. Regenerate the index after adding or retagging a rule.

## Writing memory

- `remember` captures one fact or rule and files it by scope and workflow.
- `promote-facts-rules` moves work item entries to the expert files at the end of a work item.
- `integrate-docs` imports entries in bulk from documents.
- `memory-optimize` analyzes the files for size, duplicates, and missing metadata.

All four use `### YYYY-MM-DD: Title` entry headers; see the format in `MEMORY-INDEX.md`.
