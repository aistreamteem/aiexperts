# How Memory Loading Works

**Question:** How does the agent know where to look first for facts and rules?

**Answer:** This real-estate-transaction-coordinator role loads **operations memory** for every Work Item, plus that Work Item’s own facts/rules.

---

## Discovery

### Step 1 — Index

Always load `facts/MEMORY-INDEX.md` first.

### Step 2 — Workflow context

Identify the current Work Item from `.cursor/active-context.txt` (`work-item:<id>`). Fall back to `.cursor/active-work-item.txt` only when reading old copies; do not write the legacy file.

| Session | Directory | Memory to load |
| --- | --- | --- |
| Transaction Work Item | `work-items/<id>/` | `facts-operations.md` + `rules-operations.md` + optional `work-items/<id>/facts/` |

Read **Workflow type** from `journals/work-items/<id>/progress.md` to know which registered job is active (`dates-calendar`, `missing-docs`, …). That selects the workflow **instruction file**, not a different facts file. Default if ambiguous: **operations + dates-calendar job**.

### Step 3 — Filter inside operations files

Include an entry if `**Workflows:**` is `all` or lists the current job. Work Item facts/rules are not filtered; they belong to this pack.

### Step 4 — Tools on demand

Load `docs/tools/<name>.md` only when the workflow step names that tool.

---

## Why this shape

This Expert is one role: real estate transaction coordinator (file completeness). Splitting developer vs incident files would hide dates, disclosure, HOA, and must-never rules. Growth stays in the operations pair; **memory-optimize** watches line count there.

---

## Configuration (`AGENTS.md`)

At the start of each session or skill: (1) load `facts/MEMORY-INDEX.md`, (2) load operations facts and rules, (3) load the active Work Item facts/rules, (4) follow `docs/role/work-item-method.md` and the selected `.cursor/workflows/<job>.md`.
