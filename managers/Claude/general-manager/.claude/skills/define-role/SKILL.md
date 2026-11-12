---
name: define-role
description: "Use when the operator says define my role, or when MyRole.txt says Role status: pending. Asks for the specific job, workflows, skills, and existing notes, then waits for approval."
trigger: User says "define my role", or Role status is pending
---

# Define role

Specializes this General Manager expert. The folder stays this manager type. The answers define the specific job.

## When to use

- `MyRole.txt` contains `Role status: pending`
- The operator says "define my role" (run again even if status is already defined or skipped)

## State file

`docs/role/role-definition.md` holds the questions, the answers, the note sources, the draft workflows, and the draft skills. Create it on the first question.

## Rules

- Ask one question at a time. Record the answer before the next question.
- The word continue is not an answer and is not approval.
- "I have no notes" is a real answer.
- People-sensitive notes (private conversations, performance, personal circumstances) are not stored in expert-role memory unless the operator explicitly says to store them.

## Questions, in order

   - What is your exact title, and who does this role serve?
   - What is this role accountable for?
   - Which decisions can this role make, and which must someone else approve?
   - What does a normal week include?
   - Which starter workflows match that week, and what recurring work do they miss?
   - Which starter skills are required, and which must this expert not use?
   - What must this expert never do?
   - Who decides, and what must they see before they decide?
   - What cadence already exists for this outcome?
   - Which people topics must stay private?
- Notes: ask for file paths, pasted text, or both. Examples for this role: operating cadences, decision logs, and stakeholder notes. Accept further batches until the operator says the notes are complete.

## After the notes

1. For each batch, follow integrate-docs and remember. Classify each item as a fact or a rule. Assign `management-initiative`, `management-escalation`, or both. Show the proposed entries and store only the ones the operator confirms.
2. If a note implies a workflow or skill the starter pack does not have, put that proposal in the draft. Do not add it to the registry yet.
3. Draft `docs/role/role-definition.md` with: title, who the role serves, responsibilities, decision rights, out of scope, workflows, skills required for each workflow, skills not used, and the list of remembered notes.
4. A missing recurring workflow is drafted as a third pipeline: when to use, phases, gates, artifacts, and skills.
5. Ask the operator to reply "I approve the role" or to correct the draft. "Skip role definition" keeps the starter pack, leaves confirmed note entries in place, and sets `Role status: skipped`.

## On approval

- Rewrite `MyRole.txt` from the draft and set `Role status: defined`.
- Update `.claude/workflows/workflow-registry.json` so only approved workflows remain. Add a third workflow file only if the draft included one and the operator approved it.
- Write `.claude/role-skills.md` with each skill marked required or not used. Do not delete a skill marked not used.
- Keep the questions, answers, and note sources in `docs/role/role-definition.md`.
