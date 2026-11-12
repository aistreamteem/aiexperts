---
name: operator-qa
description: >-
  Runs a self-contained question-and-answer session with the human operator to
  clarify authorization, AVL, price file, receiving difference, or notes before
  persisting them.
trigger: Clarify, verify with operator, or operator asks for Q&A
---

# Operator Q&A

## Purpose

Hold a focused Q&A session. Keep turns in a session journal. When it ends, extract answers into conclusions that drive the next purchasing step (confirm authorization, AVL status, a price file, a receiving difference, or persist a fact/rule).

## Work item branch

Keep the question transcript in this session journal. Present a fixed choice with **AskQuestion**. Ask an open-ended question in chat. When a question blocks the current work item, also add a node on that work item's map. The node id is unique and is not `work-item` or a phase name. Store the session id on the node and make it the active leaf through journal-keeper. When the session closes, store the decision and run the journal-keeper answer transition so `active` leaves this question.

## Session location

Sessions live at the expert root under `qa-sessions/`.

Active session id file: `.cursor/active-qa-session.txt`

Ids are `Q` plus a counter: `Q1`, `Q2`, …

Copy `qa-sessions/_TEMPLATE/` to `qa-sessions/<id>/` when opening a session.

## When to use

- Confirm which PO, RFQ, match, or receiving event this pack is for
- Verify a vendor name against their AVL export
- Confirm a missing quote, authorization, or receiving file
- Confirm a receiving short or match exception stays visible
- Verify notes before **remember**
- Operator says ask me / clarify / Q&A / verify this

Initiate on your own when a human answer would change the pack. Prefer this skill over inventing shop practice.

Do not use this skill for a workflow step that already has a clear next action and no blocking ambiguity.

## Phases

Follow Open → Ask → Record → Close as in the template journals.

**Forward actions** after close must be purchasing next steps, for example:

- Put the AVL export in `work-items/<id>/in/` and **continue** the first workflow step
- Run **remember** with the verified wording
- Start or switch to a Work Item for the named PO
- Resume `avl-check` / `match` / other selected job

Do not forward to software design, HLD approval, or deleted process skills.

## Examples

**Authorization before treating a PO as issued**

1. Open Q2 with purpose “confirm who may approve this amount”.
2. AskQuestion: `Use the saved approval matrix`, `Buyer may not issue this amount (keep as draft)`, `Defer`.
3. Close → continue `blanket-release` or leave the PO labeled draft.

**Verify before remember**

1. Open Q4 with outcome `notes`.
2. AskQuestion: persist “Acme Fasteners LLC is the AVL name” as an expert-role fact? `Yes`, `Yes, I will edit`, `No`, `Defer`.
3. Close → **remember** with verified wording.

**Receiving short**

1. Ask whether to leave a short of 12 pieces visible or wait for a late packing slip.
2. Close → next action is finish the short pack with the short labeled, not received-in-full.
