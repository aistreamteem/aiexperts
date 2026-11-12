# Trigger Index (action -> rules)

> **GENERATED FILE – do not hand-edit.** Regenerate with `python scripts/memory/build_trigger_index.py` after adding or retagging a rule.
>
> This is the **action axis** of the expert memory. Each rule carries a **Triggers:** field naming the tool-action(s) that should surface it. The PreToolUse hook `.cursor/hooks/inject_rules_on_action.py` reads this map and injects the matching rule text at the moment of the action – in **any** workflow, not just the one the rule is filed under. See [MEMORY-INDEX.md](MEMORY-INDEX.md) for the workflow (browsing) axis.

Indexed 10 rules across 3 files; 5 active trigger tokens; 0 rules with no Triggers field.

## milestone:review (2)

- [The named approver accepts the milestone](rules-program-delivery.md#2026-10-08-the-named-approver-accepts-the-milestone) — rules-program-delivery.md:57
- [State which milestone moved](rules-program-escalation.md#2026-10-08-state-which-milestone-moved) — rules-program-escalation.md:3

## raid:update (2)

- [Every risk has an owner and a date](rules-program-delivery.md#2026-10-08-every-risk-has-an-owner-and-a-date) — rules-program-delivery.md:39
- [Watch the dependency after the decision](rules-program-escalation.md#2026-10-08-watch-the-dependency-after-the-decision) — rules-program-escalation.md:75

## scope:change (2)

- [Scope changes use the change gate](rules-program-delivery.md#2026-10-08-scope-changes-use-the-change-gate) — rules-program-delivery.md:3
- [Response approval comes first](rules-program-escalation.md#2026-10-08-response-approval-comes-first) — rules-program-escalation.md:39

## status:report (1)

- [Status is done, next, and blocked](rules-program-delivery.md#2026-10-08-status-is-done-next-and-blocked) — rules-program-delivery.md:21

## steering:pack (3)

- [Steering packs match the plan](rules-program-delivery.md#2026-10-08-steering-packs-match-the-plan) — rules-program-delivery.md:75
- [List options and the decider](rules-program-escalation.md#2026-10-08-list-options-and-the-decider) — rules-program-escalation.md:21
- [Tell steering what was decided](rules-program-escalation.md#2026-10-08-tell-steering-what-was-decided) — rules-program-escalation.md:57
