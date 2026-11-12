# How Memory Loading Works

**Question:** How does the agent know where to look first for facts and rules?

**Answer:** This shipping / fulfillment role loads **shared** memory (always) and **operations** memory for every Work Item, plus that Work Item’s own facts/rules.

---

## Discovery

### Step 1 — Index

Always load `facts/MEMORY-INDEX.md` first.

### Step 2 — Workflow context

Identify the current Work Item from `.cursor/active-context.txt` (`work-item:<id>`), with `.cursor/active-work-item.txt` as a legacy read fallback.

| Session | Directory | Memory to load |
| --- | --- | --- |
| Shipping Work Item | `work-items/<id>/` | `facts-shared.md` + `rules-shared.md` + `facts-operations.md` + `rules-operations.md` + optional `work-items/<id>/facts/` |

Read **Workflow type** from `journals/work-items/<id>/progress.md` to know which registered job is active (`bol-pack`, `pick-wave`, …). That selects the workflow **instruction file**, not a different facts file.

### Step 3 — Filter inside memory files

Include a shared entry always. Include an operations entry if `**Workflows:**` is `all` or lists the current job. Work Item facts/rules are not filtered; they belong to this pack.

### Step 4 — Tools on demand

Load `docs/tools/<name>.md` only when the workflow step names that tool.

---

## Why this shape

This Expert is one role: shipping / fulfillment. Splitting developer vs incident files would hide the scale, BOL, hold, and short-ship rules. New cross-job (`Workflows: all`) captures go in the **shared** pair; job-tagged captures stay in **operations**. **memory-optimize** watches line count.

---

## Configuration (`AGENTS.md`)

At the start of each session or skill: (1) load `facts/MEMORY-INDEX.md`, (2) load shared then operations facts and rules, (3) load the active Work Item facts/rules, (4) follow `docs/role/work-item-method.md` and the selected `.cursor/workflows/<job>.md`.
