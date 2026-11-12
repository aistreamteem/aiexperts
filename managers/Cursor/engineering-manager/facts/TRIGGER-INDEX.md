# Trigger Index (action -> rules)

> **GENERATED FILE – do not hand-edit.** Regenerate with `python scripts/memory/build_trigger_index.py` after adding or retagging a rule.
>
> This is the **action axis** of the expert memory. Each rule carries a **Triggers:** field naming the tool-action(s) that should surface it. The PreToolUse hook `.cursor/hooks/inject_rules_on_action.py` reads this map and injects the matching rule text at the moment of the action – in **any** workflow, not just the one the rule is filed under. See [MEMORY-INDEX.md](MEMORY-INDEX.md) for the workflow (browsing) axis.

Indexed 10 rules across 3 files; 5 active trigger tokens; 0 rules with no Triggers field.

## decision:log (1)

- [Every action has an owner](rules-team-delivery.md#2026-10-08-every-action-has-an-owner) — rules-team-delivery.md:57

## escalation:open (3)

- [Name who is affected today](rules-team-escalation.md#2026-10-08-name-who-is-affected-today) — rules-team-escalation.md:3
- [Response waits for approval](rules-team-escalation.md#2026-10-08-response-waits-for-approval) — rules-team-escalation.md:21
- [Record what is watched](rules-team-escalation.md#2026-10-08-record-what-is-watched) — rules-team-escalation.md:75

## hiring:loop (2)

- [Headcount and offers wait for approval](rules-team-delivery.md#2026-10-08-headcount-and-offers-wait-for-approval) — rules-team-delivery.md:39
- [Separate the lasting staffing change](rules-team-escalation.md#2026-10-08-separate-the-lasting-staffing-change) — rules-team-escalation.md:39

## meeting:1on1 (1)

- [1:1 notes stay on the work item](rules-team-delivery.md#2026-10-08-11-notes-stay-on-the-work-item) — rules-team-delivery.md:21

## status:update (2)

- [Status leads with risk](rules-team-delivery.md#2026-10-08-status-leads-with-risk) — rules-team-delivery.md:3
- [Tell stakeholders in the same step](rules-team-escalation.md#2026-10-08-tell-stakeholders-in-the-same-step) — rules-team-escalation.md:57
