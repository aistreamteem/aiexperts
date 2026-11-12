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

## Role note

This leftover skill is not part of the registered optometry-role job maps. Prefer **workflow-selector** and `.claude/workflows/`. When the operator still points at a free-form requirements note, use neutral intake questions: what is affected, who asked or escalated, and where the evidence files are.

## Instructions

### 0. Work Item context

- Active work item: the line in `.claude/active-context.txt`, formatted `work-item:<id>`.
- Artifacts (spec, docs, TODOS, STATUS, facts): `work-items/<id>/`.
- Journal: `journals/work-items/<id>/progress.md` for item-wide fields, `state.json` for the
  branch map, and `nodes/<active leaf>.md` for step notes, open questions, and the next action.
  Write through journal-keeper.

**0a. Check if spec-parser should run for this workflow:**
  - Read journal **Workflow type** field
  - This optometry role’s registered jobs do not use the developer or production-incident pipelines. Prefer **workflow-selector** and the maps under `.claude/workflows/`.
  - If the operator still points at a free-form requirements file, continue with the neutral questions below.

1. **Load facts and rules:**
  - Load `facts/MEMORY-INDEX.md`, then `facts/facts-operations.md` + `facts/rules-operations.md`
  - Read `work-items/<id>/facts/facts.md` and `.../rules.md` when present
  - Internalize: Rules MUST be followed; Facts provide context
  - Log loaded facts/rules labels to journal via journal-keeper

### Spec Location and Creation

2. **Determine artifact path:**
  - Read `journals/work-items/<id>/progress.md` for workflow type
  - Default artifact: `work-items/<id>/docs/requirements-summary.md`
  - Ask neutral intake questions only: what is affected, who escalated or requested it, and where the evidence files are

3. **Locate or create spec file:**

  a. **Check for spec in Work Item folder first:**
  - Look for `work-items/<work-item-id>/spec.md`
  - If found, use this as the spec source

  b. **Check for spec at repo root (legacy):**
  - If not in Work Item folder, check `spec.md` at repo root
  - If found, use this as the spec source

  c. **Check journal for custom spec path:**
  - If journal has a custom spec file path, use that

  d. **If no spec file exists:**
  - Offer: provide a path, start a short Q&A into `work-items/<id>/spec.md`, or capture an informal summary under `work-items/<id>/docs/requirements-summary.md`

4. **Read the spec file** (from determined location)

5. **Cross-reference spec against loaded facts/rules:**
  - Check if any Expert Role rules constrain requirements (e.g., "must use X technology", "no Y pattern")
  - Check if any Expert Role facts provide context (e.g., "team prefers Z approach")
  - Note any conflicts or relevant constraints

6. **Ask neutral intake questions:** what is affected, who escalated or requested it, where the evidence is, success criteria, and what is out of scope.

7. Emit a requirements summary and write it to the artifact path from step 2.

8. Emit assumptions and open questions; classify each as **blocking** (major/high-risk) or **deferred** (resolve when reaching the task that needs the answer). **Flag possible blockers** the user should be aware of: external dependencies (e.g. downloads from GitHub, Hugging Face), APIs, access or credentials, so these can be discussed early and the agent and user stay in agreement.

9. Write open questions into the active node under `journals/work-items/<id>/nodes/` (Open questions blocking/deferred). Do not proceed past this phase until all blocking questions are answered by the user.

10. If the user has answered any question in this turn, record the question and answer in Resolved Q&A in the journal in the **same response** and remove it from open questions.

11. Record spec file path and last-modified (or a version) in the journal for spec-change detection. Path should be relative to repo root or indicate if spec was created via Q&A session.

### Proactive Detection

12. **Watch for new facts/rules during requirements analysis:**
  - User provides constraints not in rules (e.g., "we must use Python 3.11+")
  - User describes team practices (e.g., "we always use pytest for testing")
  - If detected, use remember skill to propose capturing

### Completion

13. After completion (and only when blocking questions are empty), set next action to the first ready step of the selected registered optometry-role job (or ask the operator which job to run).

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
