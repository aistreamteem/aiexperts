---
name: diagram-generator
description: >-
  Kept for platform compatibility. This equipment-rental expert does not run a
  software HLD/DD diagram pipeline. Prefer visual-page for operator layouts.
disable-model-invocation: false
---

# Diagram Generator

## Not used by this rental role

This expert produces reservation lists, contract packs, inspection packs, and related files. It does not maintain a software design-doc or Mermaid diagram tree.

When the operator needs a picture of a flow or layout, use **visual-page**.

### 0. Work Item context

- Active work item: the line in `.cursor/active-context.txt`, formatted `work-item:<id>`.
- Artifacts: `work-items/<id>/`.
- Journal: `journals/work-items/<id>/progress.md`, `state.json`, and `nodes/<active leaf>.md` via journal-keeper.
