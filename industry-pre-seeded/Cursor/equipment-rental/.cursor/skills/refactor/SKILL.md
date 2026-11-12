---
name: refactor
description: >-
  Kept for platform compatibility. This equipment-rental expert does not run a
  software refactor pipeline. Prefer cleaning Work Item packs and memory files.
disable-model-invocation: false
---

# Refactor

## Not used by this rental role

Do not invent a software refactor plan. For duplicate shop facts/rules, use **memory-optimize** or **promote-facts-rules**. For pack cleanup, edit files under `work-items/<id>/` and record the change with **journal-keeper**.

### 0. Work Item context

- Active work item: the line in `.cursor/active-context.txt`, formatted `work-item:<id>`.
- Artifacts: `work-items/<id>/`.
- Journal: `journals/work-items/<id>/progress.md`, `state.json`, and `nodes/<active leaf>.md` via journal-keeper.
