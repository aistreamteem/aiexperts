---
name: spec-parser
description: "Use when the user says \"start\", \"implement from spec\", or points to a requirements/spec file, or when the journal is missing. Parses the spec, raises blocking questions, and creates the journal."
disable-model-invocation: false
---

# Spec Parser

## Journal layer

Do not create a second tree. `continue` copies `journals/work-items/_TEMPLATE/`. A blocking question becomes a map node through journal-keeper and becomes the active leaf. Its id is unique and is not `work-item` or a phase name. Use AskQuestion for a fixed choice and chat for an open answer.

Parses the project specification, extracts requirements, validates, and lists assumptions and open questions. Use when starting the project, when the user points to a spec file, or when the spec has changed and must be re-parsed.

## When to use

- User says "start", "implement from spec", or points to a requirements/spec file
- Pipeline is at spec phase or journal says next action is "run spec-parser"
- User indicates the spec has changed and must be re-parsed

## Role behavior

This Expert is a self-storage office role. Spec-parser is only for an optional short job brief when the operator brings a requirements note. Prefer **workflow-selector** / **continue** for registered jobs. Do not invent a developer or production-incident pipeline.

Artifact path when used: `work-items/<id>/docs/design/requirements-summary.md`

Neutral clarifying questions (adapt to the job):
- What unit, date, or pack is affected?
- Who has escalated or asked for this pack?
- Where is the evidence (export, PDF, checklist) in `in/`?

## Instructions

### Work Item Context & Facts/Rules Loading

0. **Get Work Item context:**
  - Active work item: the line in `.cursor/active-context.txt`, formatted `work-item:<id>`.
  - Artifacts (spec, docs, TODOS, STATUS, facts): `work-items/<id>/`.
  - Journal: `journals/work-items/<id>/progress.md` for item-wide fields, `state.json` for the
    branch map, and `nodes/<active leaf>.md` for step notes, open questions, and the next action.
    Write through journal-keeper.

**0a. Check if spec-parser should run:**
  - Read journal **Workflow type** field
  - For registered storage-office jobs, prefer the workflow map; only run this skill when the operator pointed at a requirements/spec note
  - Check MyRole.txt if unsure whether a free-form brief is in scope

1. **Load facts and rules:**
  - Load `facts/MEMORY-INDEX.md` first, then `facts/facts-shared.md` + `facts/rules-shared.md`
  - Read `work-items/<work-item-id>/facts/facts.md` (Work Item facts, if any exist yet)
  - Read `work-items/<work-item-id>/facts/rules.md` (Work Item rules, if any exist yet)
  - Internalize: Rules MUST be followed; Facts provide context
  - Log loaded facts/rules labels to journal via journal-keeper

### Spec Location and Creation

2. **Artifact path:** `work-items/<work-item-id>/docs/design/requirements-summary.md`

3. **Locate or create spec file:**

  a. **Check for spec in Work Item folder first:**
  - Look for `work-items/<work-item-id>/spec.md`
  - If found, use this as the spec source

  b. **Check for spec at repo root (legacy):**
  - If not in Work Item folder, check `spec.md` at repo root
  - If found, use this as the spec source

  c. **Check journal for custom spec path:**
  - If journal has a custom spec file path, use that

  d. **If no spec file exists:** offer options below

**No spec found - offer options:**
  - Ask user: "No spec.md file found. Would you like to:"
  - Option 1: "Provide a path to an existing spec file"
  - Option 2: "Begin a short Q&A to create spec.md"
  - Option 3: "Skip spec and name the registered workflow instead"

**If user chooses Option 2 (Q&A session):**
  - What pack is needed? (occupancy, late list, move-in packet, auction file, …)
  - Which unit, date, or export is in scope?
  - What must be present vs missing?
  - What is out of scope?
  - Write completed brief to `work-items/<work-item-id>/spec.md`

**If user chooses Option 3:**
  - Invoke **workflow-selector** and stop

4. **Read the spec file** (from determined location)

5. **Cross-reference spec against loaded facts/rules**

6. **Ask clarifying questions** using the neutral list above when needed

7. Emit a requirements summary to `docs/design/requirements-summary.md` under the Work Item

8. Emit assumptions and open questions; classify each as **blocking** or **deferred**

9. Write open questions into the active node via journal-keeper. Do not proceed past this phase until all blocking questions are answered.

10. If the user has answered any question in this turn, record it in Resolved Q&A in the **same response**

11. Record spec file path in the journal

### Proactive Detection

12. **Watch for new facts/rules** and propose **remember** when the operator teaches shop procedure

### Completion

13. After completion (blocking questions empty), set next action to the first ready YAML step of the selected registry workflow, or “run workflow-selector” if none is set. Do not set next action to missing developer phase skills.

14. Update the journal via journal-keeper with phase completed, artifacts, and facts/rules loaded.

## Spec Q&A Session Example

When conducting a spec Q&A session to create spec.md, follow this structured approach:

**Step 1: Problem Statement**
- "What problem are you trying to solve?"
- "Who is affected by this problem?"

**Step 2: Solution Overview**
- "What solution do you envision?"
- "What are the key capabilities/features needed?"

**Step 3: Users & Stakeholders**
- "Who will use this?"
- "Are there different user roles?"

**Step 4: Constraints**
- "Are there technology constraints? (e.g., must use .NET, Python, cloud platform)"
- "Are there timeline or budget constraints?"
- "Any compliance or security requirements?"

**Step 5: Success Criteria**
- "How will you know this is successful?"
- "What metrics or outcomes define success?"

**Step 6: Scope Boundaries**
- "What is explicitly out of scope?"
- "What can be deferred to future phases?"

**Step 7: Dependencies**
- "Are there external systems to integrate with?"
- "Any third-party services or APIs?"
- "Any existing codebases or data sources?"

After gathering answers, synthesize into a structured spec.md with sections:
- Problem Statement
- Solution Overview
- Users & Stakeholders
- Requirements (Functional & Non-Functional)
- Constraints
- Success Criteria
- Out of Scope
- Dependencies & Integrations
- Assumptions
