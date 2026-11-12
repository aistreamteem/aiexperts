---
name: spec-parser
description: "Use when the user says \"start\", \"implement from spec\", or points to a requirements/spec file, or when the journal is missing. Parses the spec, raises blocking questions, and creates the journal."
disable-model-invocation: false
---

### 0. Work Item context

- Active work item: the line in `.cursor/active-context.txt`, formatted `work-item:<id>`.
- Artifacts (spec, docs, TODOS, STATUS, facts): `work-items/<id>/`.
- Journal: `journals/work-items/<id>/progress.md` for item-wide fields, `state.json` for the
  branch map, and `nodes/<active leaf>.md` for step notes, open questions, and the next action.
  Write through journal-keeper.


# Spec Parser

## Journal layer

Do not create a second tree. `continue` copies `journals/work-items/_TEMPLATE/`. A blocking question becomes a map node through journal-keeper and becomes the active leaf. Its id is unique and is not `work-item` or a phase name. Use AskQuestion for a fixed choice and chat for an open answer.

Parses the project specification, extracts requirements, validates, and lists assumptions and open questions. Use when starting the project, when the user points to a spec file, or when the spec has changed and must be re-parsed.

## When to use

- User says "start", "implement from spec", or points to a requirements/spec file
- Pipeline is at spec phase or journal says next action is "run spec-parser"
- User indicates the spec has changed and must be re-parsed

## Workflow-Aware Behavior

This role uses registered CSR jobs, not a developer or incident pipeline. Prefer **workflow-selector** and the matching `.cursor/workflows/<id>.md` file. Use this skill only when the operator pastes a short job brief that still needs open questions before the first YAML step.

Neutral intake questions (adapt to the selected registry job):
- What is affected (client, policy, holder, date range)?
- Who has escalated or is waiting on the pack?
- Where is the source evidence (AMS export, PDF, spreadsheet path under `in/`)?

## Instructions

### Work Item Context & Facts/Rules Loading

0. **Get Work Item context:**
  - Read active Work Item ID from `.cursor/active-context.txt` (`work-item:<id>`; legacy read fallback only)
  - Work Item paths: `work-items/<work-item-id>/[path]`
  - Journal: `journals/work-items/<work-item-id>/progress.md`

**0a. Check if spec-parser should run for this workflow:**
  - Read journal **Workflow type** field (a registry id such as `coi-request-pack`)
  - If the job already has a clear next YAML step, skip this skill and run **continue**
  - Do not route into a developer or production-incident pipeline

1. **Load facts and rules:**
  - Load `facts/MEMORY-INDEX.md`, then `facts/facts-operations.md` and `facts/rules-operations.md`
  - Read `work-items/<work-item-id>/facts/facts.md` (Work Item facts, if any exist yet)
  - Read `work-items/<work-item-id>/facts/rules.md` (Work Item rules, if any exist yet)
  - Internalize: Rules MUST be followed; Facts provide context
  - Log loaded facts/rules labels to journal via journal-keeper

### Spec Location and Creation

2. **Determine artifact path:**
  - Read `journals/work-items/<work-item-id>/progress.md` to get workflow type
  - Default brief path for this role: `work-items/<work-item-id>/PURPOSE.md` or the operator’s pasted brief in chat
  - Do not invent `docs/design/` or `docs/incident/` paths for this CSR role

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
  - Prefer registered CSR workflows; use this brief only to unblock the first YAML step
  - Capture open questions before inventing shop procedure

**No spec found - offer options:**
  - Ask user: "No spec.md file found. Would you like to:"
  - Option 1: "Provide a path to an existing spec file"
  - Option 2: "Begin a specification Q&A session to create spec.md"
  - Option 3: "Skip spec and provide requirements informally"

**If user chooses Option 2 (Q&A session):**
  - Conduct structured requirements gathering via questions:
  - What problem does this solve? (Problem statement)
  - Who are the users/stakeholders?
  - What are the key features/capabilities?
  - What are the constraints? (technology, timeline, budget, compliance)
  - What are the success criteria?
  - What is out of scope?
  - Any dependencies or integrations?
  - As user answers, build spec content incrementally
  - Write completed spec to `work-items/<work-item-id>/spec.md`
  - Confirm: "Created spec.md at work-items/<work-item-id>/spec.md"

**If user chooses Option 3 (informal):**
  - Gather requirements conversationally
  - Document in `work-items/<work-item-id>/docs/design/requirements-summary.md` directly
  - Note in journal: "No formal spec; requirements captured informally"

4. **Read the spec file** (from determined location)

5. **Cross-reference spec against loaded facts/rules:**
  - Check if any Expert Role rules constrain requirements (e.g., "must use X technology", "no Y pattern")
  - Check if any Expert Role facts provide context (e.g., "team prefers Z approach")
  - Note any conflicts or relevant constraints

6. **Ask workflow-specific questions:**
  - For all workflows: Standard requirement questions (what, why, constraints, success criteria)
  - Add neutral intake questions (what is affected, who escalated, where the evidence is) if not already captured by workflow-selector

7. Emit a requirements summary and write it to the workflow-specific artifact path (from step 2).

8. Emit assumptions and open questions; classify each as **blocking** (major/high-risk) or **deferred** (resolve when reaching the task that needs the answer). **Flag possible blockers** the user should be aware of: external dependencies (e.g. downloads from GitHub, Hugging Face), APIs, access or credentials, so these can be discussed early and the agent and user stay in agreement.

9. Write open questions into `journals/work-items/<work-item-id>/progress.md` under Open questions (blocking) and Open questions (deferred). Do not proceed past this phase until all blocking questions are answered by the user.

10. If the user has answered any question in this turn, record the question and answer in Resolved Q&A in the journal in the **same response** and remove it from open questions.

11. Record spec file path and last-modified (or a version) in the journal for spec-change detection. Path should be relative to repo root or indicate if spec was created via Q&A session.

### Proactive Detection

12. **Watch for new facts/rules during requirements analysis:**
  - User provides constraints not in rules (e.g., "we must use Python 3.11+")
  - User describes team practices (e.g., "we always use pytest for testing")
  - If detected, use remember skill to propose capturing

### Completion

13. After completion (and only when blocking questions are empty), set next action based on **Workflow type** field in journal:
  - **CSR registry job:** "run continue" (first ready YAML step of the selected workflow)
  - **Custom pipeline (legacy):** Next phase from MyRole.txt definition

14. Update the journal via journal-keeper with phase completed, artifacts (including spec file location and workflow-specific artifact path), facts/rules loaded.

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