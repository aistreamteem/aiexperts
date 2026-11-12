---
name: integrate-docs
description: "Use when the operator provides notes, exports, or write-ups to fold into facts, rules, and MyRole.txt."
trigger: User provides notes or says integrate this
---

# Integrate documents

Use this when define-role collects existing notes, and whenever the operator supplies a file or pasted text to remember.

## Steps

1. Ask for file paths, pasted text, or both, plus an optional hint about the topic. "I have no notes" means stop.
2. Read every path. Split the material into facts and rules.
   - Facts: who decides, cadence, stakeholders, historical outcomes, where trackers live.
   - Rules: how status is written, how a decision is recorded, what must be approved, who must be told.
3. Assign each entry to `program-delivery`, `program-escalation`, or `all`. Set triggers from: status:report, raid:update, milestone:review, scope:change, steering:pack, write:doc. Every rule needs a `**Triggers:**` line (`none` when no action should surface it).
4. Hold back people-sensitive notes unless the operator explicitly says to store them in expert-role memory.
5. Show the proposed entries. Store only confirmed ones: `Workflows: all` goes to `facts/facts-shared.md` or `facts/rules-shared.md`; otherwise the matching `facts/facts-*.md` or `facts/rules-*.md` workflow file.
6. If a note describes a recurring workflow the registry does not have, propose it for MyRole.txt and, during define-role, put it in the role draft. Do not enable it before approval.
7. Update `facts/MEMORY-INDEX.md` when a new topic needs a pointer.
8. Summarize what was stored, what was skipped, and which files changed. Regenerate the trigger index when rules changed.
