# How Memory Loading Works

**Question:** How does the agent know where to look first for facts and rules?

**Answer:** This moving-company office role always loads **shared** memory, then **operations** memory, plus the active Work Item pair. It does not load developer or production-incident files.

---

## Discovery

### Step 1: Load this navigation index

Always load `facts/MEMORY-INDEX.md` first.

### Step 2: Determine Work Item and job

| Session | Directory | Memory files |
| --- | --- | --- |
| Role job | `work-items/<id>/` | shared + operations + Work Item `facts/` pair |

Detection:

1. `.claude/active-context.txt` (legacy read fallback: `.claude/active-work-item.txt`)
2. `journals/work-items/<id>/progress.md` **Workflow type** (registered job id)
3. Default new job: `estimate-from-rate-file` (see `docs/role/work-item-method.md`)

### Step 3: Load shared, operations, then Work Item

```
1. MEMORY-INDEX.md
2. facts-shared.md
3. rules-shared.md
4. facts-operations.md
5. rules-operations.md
6. work-items/<id>/facts/facts.md (if present)
7. work-items/<id>/facts/rules.md (if present)
```

Filter Expert Role entries by `**Workflows:**` (`all` or the current job id). New `Workflows: all` captures go in the shared pair.

### Step 4: Tools on demand

`docs/tools/` files load when the current workflow step names them. Large reference material is not auto-loaded.

---

## Action axis

When the agent is about to write a CSV, estimate artifact, or pack markdown, the PreToolUse hook `.claude/hooks/inject_rules_on_action.py` injects matching rules from `facts/trigger-index.json` regardless of the current workflow.

## Maintenance

Run `py -3 .claude/skills/memory-optimize/scripts/analyze-memory.py facts`. Keep starter notes labeled as guesses until the operator confirms them.
