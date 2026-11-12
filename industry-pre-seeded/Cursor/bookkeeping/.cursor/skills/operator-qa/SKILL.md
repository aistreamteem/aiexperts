---
name: operator-qa
description: >-
  Runs a self-contained question-and-answer session with the human operator to
  clarify period, account, shop practice, or notes before persisting them.
trigger: Clarify, verify with operator, or operator asks for Q&A
---

# Operator Q&A

## Purpose

Hold a focused Q&A session. Keep turns in a session journal. When it ends, extract answers into conclusions that drive the next bookkeeping step (confirm period, accept a labeled guess, verify a rec exception, or persist a fact/rule).

## Work item branch

Keep the question transcript in this session journal. Present a fixed choice with **AskQuestion**. Ask an open-ended question in chat. When a question blocks the current work item, also add a node on that work item's map. The node id is unique and is not `work-item` or a phase name. Store the session id on the node and make it the active leaf through journal-keeper. When the session closes, store the decision and run the journal-keeper answer transition so `active` leaves this question.

## Session location

Sessions live at the expert root under `qa-sessions/`.

Active session id file: `.cursor/active-qa-session.txt`

Ids are `Q` plus a counter: `Q1`, `Q2`, …

Copy `qa-sessions/_TEMPLATE/` to `qa-sessions/<id>/` when opening a session.

## When to use

- Confirm entity, period, or which bank/card this pack is for
- Verify a labeled account guess vs their chart
- Confirm a rec difference, missing bill, or personal charge
- Verify notes before **remember**
- Operator says ask me / clarify / Q&A / verify this

Initiate on your own when a human answer would change the pack. Prefer this skill over inventing shop practice.

Do not use this skill for a workflow step that already has a clear next action and no blocking ambiguity.

## Phases

Follow Open → Ask → Record → Close as in the template journals.

**Forward actions** after close must be bookkeeping next steps, for example:

- Put the statement CSV in `work-items/<id>/in/` and **continue** the first workflow step
- Run **remember** with the verified wording
- Start or switch to a Work Item for the named period
- Resume `bank-reconcile` / `month-end` / other selected job

Do not forward to software design, HLD approval, or deleted process skills.

## Examples

**Period before batch**

1. Open Q2 with purpose “confirm statement dates before coding”.
2. AskQuestion: `Use statement 2026-08-01 to 2026-08-31`, `Different range (I will type it)`, `Defer`.
3. Close → continue `credit-card-code` or `bank-review` on that period.

**Verify before remember**

1. Open Q4 with outcome `notes`.
2. AskQuestion: persist “Rent vendors → 6100” as an expert-role fact? `Yes`, `Yes, I will edit`, `No`, `Defer`.
3. Close → **remember** with verified wording.

**Rec exception**

1. Ask whether to leave a $42.17 difference visible or wait for a missing fee line.
2. Close → next action is finish the rec pack with the difference labeled, not a plug.
