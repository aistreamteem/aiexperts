---
name: operator-qa
description: >-
  Runs a self-contained question-and-answer session with the human operator to
  clarify clinic date, which remaining file is live, shop practice, or notes
  before persisting them.
trigger: Clarify, verify with operator, or operator asks for Q&A
---

# Operator Q&A

## Purpose

Hold a focused Q&A session. Keep turns in a session journal. When it ends, extract answers into conclusions that drive the next front-role step (confirm clinic date, which remaining column is live, missing referral page, or persist a fact/rule).

## Work item branch

Keep the question transcript in this session journal. Present a fixed choice with **AskUserQuestion**. Ask an open-ended question in chat. When a question blocks the current work item, also add a node on that work item's map. The node id is unique and is not `work-item` or a phase name. Store the session id on the node and make it the active leaf through journal-keeper. When the session closes, store the decision and run the journal-keeper answer transition so `active` leaves this question.

## Session location

Sessions live at the expert root under `qa-sessions/`.

Active session id file: `.claude/active-qa-session.txt`

Ids are `Q` plus a counter: `Q1`, `Q2`, …

Copy `qa-sessions/_TEMPLATE/` to `qa-sessions/<id>/` when opening a session.

## When to use

- Confirm clinic date, location, or which tracker/export this pack is for
- Two dated remaining or eligibility files disagree
- Missing auth letter, POC signature, or named HEP PDF
- Verify notes before **remember**
- Operator says ask me / clarify / Q&A / verify this

Initiate on your own when a human answer would change the pack. Prefer this skill over inventing clinic procedure.

Do not use this skill for a workflow step that already has a clear next action and no blocking ambiguity.

## Phases

Follow Open → Ask → Record → Close as in the template journals.

**Forward actions** after close must be this role’s next steps, for example:

- Put the schedule or tracker in `work-items/<id>/in/` and **continue** the first workflow step
- Run **remember** with the verified wording
- Start or switch to a Work Item for the named clinic date
- Resume `day-list` / `auth-remaining-from-file` / other selected job

Do not forward to software design or deleted process skills.

## Examples

**Which remaining file is live**

1. Open Q2 with purpose “confirm remaining column before listing visits left”.
2. AskUserQuestion: `Use Thursday tracker screenshot`, `Use visit-count export`, `Quote both and I will pick`, `Defer`.
3. Close → continue `auth-remaining-from-file` on the chosen file.

**Verify before remember**

1. Open Q4 with outcome `notes`.
2. AskUserQuestion: persist “This clinic’s cancel window is 24 hours” as an expert-role fact? `Yes`, `Yes, I will edit`, `No`, `Defer`.
3. Close → **remember** with verified wording.

**Missing referral page**

1. Ask whether to mark the packet incomplete or wait for a named page they will drop.
2. Close → next action is finish the completeness pack with the missing page labeled, not invent the form.
