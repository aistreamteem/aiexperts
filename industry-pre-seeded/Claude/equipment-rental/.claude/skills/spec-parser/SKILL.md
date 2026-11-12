---
name: spec-parser
description: >-
  Kept for platform compatibility. This equipment-rental expert does not run a
  software spec→HLD pipeline. Use workflow-selector and the registered job files.
disable-model-invocation: false
---

# Spec Parser

## Not used by this rental role

Do not invent a software requirements summary. Prefer:

1. **workflow-selector** to pick a registered job
2. The matching `.claude/workflows/<job>.md` file
3. Operator questions about what unit/day/contract is affected, who holds the gate, and where the export or PDF evidence is

### 0. Work Item context

- Active work item: the line in `.claude/active-context.txt`, formatted `work-item:<id>`.
- Artifacts: `work-items/<id>/`.
- Journal: `journals/work-items/<id>/progress.md`, `state.json`, and `nodes/<active leaf>.md` via journal-keeper.
- Memory: `facts/MEMORY-INDEX.md`, then `facts/facts-shared.md` + `facts/rules-shared.md`.
