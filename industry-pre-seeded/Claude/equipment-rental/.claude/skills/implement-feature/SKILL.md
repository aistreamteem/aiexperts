---
name: implement-feature
description: >-
  Kept for platform compatibility. This equipment-rental expert does not implement
  software TODOS tasks. Follow the registered rental workflow steps instead.
disable-model-invocation: false
---

# Implement Feature

## Not used by this rental role

Do not run a software task loop. Perform one ready step from the selected `.claude/workflows/` file and update the journal with **journal-keeper**.

### 0. Work Item context

- Active work item: the line in `.claude/active-context.txt`, formatted `work-item:<id>`.
- Artifacts: `work-items/<id>/`.
- Journal: `journals/work-items/<id>/progress.md`, `state.json`, and `nodes/<active leaf>.md` via journal-keeper.
- Memory: `facts/MEMORY-INDEX.md`, then `facts/facts-shared.md` + `facts/rules-shared.md`.
