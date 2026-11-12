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

## Role-aware behavior

This pest-control office expert does not run a software-build or production-incident pipeline. Prefer **workflow-selector** / **continue** for registered pest-office jobs. If the operator still points at a free-form brief or checklist, treat it as intake notes for the active Work Item and ask neutral clarifying questions:

- What is affected (route day, ticket pack, log pack, map set, WDO folder, estimate)?
- Who has escalated or is waiting on the pack?
- Where is the evidence (which file under `in/`)?

## Instructions

### Work Item Context & Facts/Rules Loading

0. **Get Work Item context:**
  - Active work item: the line in `.cursor/active-context.txt`, formatted `work-item:<id>`.
  - Artifacts (spec, docs, TODOS, STATUS, facts): `work-items/<id>/`.
  - Journal: `journals/work-items/<id>/progress.md` for item-wide fields, `state.json` for the
    branch map, and `nodes/<active leaf>.md` for step notes, open questions, and the next action.
    Write through journal-keeper.

**0a. Check if spec-parser should run for this workflow:**
  - Read journal **Workflow type** field
  - For registered pest-office jobs, prefer **continue** walking the workflow YAML — skip inventing a design-doc pipeline
  - If the operator explicitly asked to parse a brief into Work Item notes, continue below

1. **Load facts and rules:**
  - Load `facts/MEMORY-INDEX.md`, then `facts/facts-operations.md` and `facts/rules-operations.md`
  - Read `work-items/<id>/facts/facts.md` and `.../rules.md` when present
  - Internalize: Rules MUST be followed; Facts provide context
  - Log loaded facts/rules labels to journal via journal-keeper

### Spec Location and Creation

2. **Determine note path for this Work Item:**
  - Prefer `work-items/<id>/work/brief-notes.md` (or an existing checklist they dropped in `in/`)
  - Do not invent `docs/design/` or `docs/incident/` trees for this role

3. **Locate or create the brief:**

  a. Look for `work-items/<id>/spec.md` or a checklist under `in/`
  b. If journal has a custom brief path, use that
  c. If nothing exists, ask:
     - Provide a path to an existing brief/checklist, or
     - Answer short intake questions (what pack, which files, who is waiting), or
     - Skip and run **workflow-selector** / **continue** instead

4. **Read the brief** (from the determined location)

5. **Cross-reference against loaded operations facts/rules** (never invent mix/EPA, never diagnose, no gate codes, skip list wins)

6. **Ask neutral clarifying questions** when needed: what is affected, who escalated, where the evidence file is

7. Write a short summary under `work-items/<id>/work/` when useful

8. Emit assumptions and open questions; classify each as **blocking** or **deferred**. Flag missing shop files early.

9. Write open questions into the active node under `journals/work-items/<id>/nodes/`. Do not proceed past blocking questions until answered.

10. If the user answered in this turn, record Resolved Q&A in the same response.

11. Record the brief path in the journal via journal-keeper.

### Proactive Detection

12. Watch for shop corrections worth **remember** (required log fields, skip labels, “never” constraints).

### Completion

13. After blocking questions are empty, set next action to the first ready YAML step of the selected pest-office workflow (or **workflow-selector** if none).

14. Update the journal via journal-keeper with artifacts and facts/rules loaded.

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
