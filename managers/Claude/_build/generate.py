"""Generate four manager experts under D:\\ManagerAIExperts."""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from roles import ROLES  # noqa: E402

SRC = Path(r"D:\ClaudeAIExpert")
OUT = Path(r"D:\ManagerAIExperts")
DATE = "2026-10-08"

FORBIDDEN = [
    "hld-writer",
    "dd-writer",
    "scaffold-project",
    "implement-feature",
    "iterative-feature",
    "facts-developer",
    "HLD",
    "DD",
    "pytest",
    "NUnit",
    "venv",
    "NuGet",
    "feature/WID",
    "OAuth",
    "PostgreSQL",
    "repository pattern",
    "write:sql",
    "pr:open",
]


def ul(items):
    return "\n".join(f"- {item}" for item in items)


def w(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8", newline="\n")


def skill(name, description, trigger, body):
    return f"""---
name: {name}
description: "{description}"
trigger: {trigger}
---

{body.strip()}
"""


def bullets_numbered(items):
    return "\n".join(f"{i}. {item}" for i, item in enumerate(items, 1))


def mem_fact(role, fact):
    wf = role["planned_key"] if fact["workflows"] == "planned" else role["esc_key"]
    return f"""### {DATE}: {fact['title']}

**Scope:** expert-role

**Workflows:** {wf}

**Captured:** {DATE}

**Source:** starter pack

{fact['body']}
"""


def mem_rule(role, rule):
    wf = role["planned_key"] if rule["workflows"] == "planned" else role["esc_key"]
    return f"""### {DATE}: {rule['title']}

**Scope:** expert-role

**Workflows:** {wf}

**Triggers:** {rule['triggers']}

**Captured:** {DATE}

**Source:** starter pack

**Rule:** {rule['rule']}

**Why:** {rule['why']}

**How to apply:** {rule['how']}
"""


def copy_support(role, base: Path):
    hooks = base / ".claude" / "hooks"
    hooks.mkdir(parents=True, exist_ok=True)
    for name in ("merge-agent-notes.sh", "post-journal-update.sh", "on-subagent-stop.sh"):
        src = SRC / ".claude" / "hooks" / name
        dest = hooks / name
        text = src.read_text(encoding="utf-8")
        if name == "post-journal-update.sh":
            text = text.replace(
                'WORKSPACE_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"',
                'WORKSPACE_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"',
            )
        dest.write_text(text, encoding="utf-8", newline="\n")
    script_dir = base / "scripts" / "memory"
    script_dir.mkdir(parents=True, exist_ok=True)
    gen = (SRC / "scripts" / "memory" / "build_trigger_index.py").read_text(encoding="utf-8")
    gen = gen.replace(
        'RULES_FILES = ["rules-developer.md", "rules-incident-response.md", "rules-operations.md"]',
        f'RULES_FILES = ["rules-{role["planned_key"]}.md", "rules-{role["esc_key"]}.md"]',
    )
    old_doc = gen.split('"""', 2)
    # Keep the code; replace only if the docstring mentions developer session types.
    gen = gen.replace(
        "session type (developer / incident-response / operations)",
        f"session type ({role['planned_key']} / {role['esc_key']})",
    )
    gen = gen.replace(
        "write a .sql file, open a PR, change a config",
        "write a decision log, a status note, or an escalation record",
    )
    gen = gen.replace("fallback discovery path", "fallback lookup path")
    (script_dir / "build_trigger_index.py").write_text(gen, encoding="utf-8", newline="\n")
    analysis = (SRC / ".claude" / "skills" / "memory-optimize" / "scripts" / "analyze-memory.py").read_text(encoding="utf-8")
    analysis = analysis.replace(
        """    workflow_files = [
        'facts-incident-response.md',
        'facts-developer.md',
        'facts-operations.md',
        'rules-incident-response.md',
        'rules-developer.md',
        'rules-operations.md',
    ]""",
        f"""    workflow_files = [
        'facts-{role["planned_key"]}.md',
        'facts-{role["esc_key"]}.md',
        'rules-{role["planned_key"]}.md',
        'rules-{role["esc_key"]}.md',
    ]""",
    )
    dest_analysis = base / ".claude" / "skills" / "memory-optimize" / "scripts" / "analyze-memory.py"
    dest_analysis.parent.mkdir(parents=True, exist_ok=True)
    analysis = analysis.replace("YYYY-MM-DD", "year-month-day")
    dest_analysis.write_text(analysis, encoding="utf-8", newline="\n")


def emit_hooks(role, base: Path):
    planned = role["planned_key"]
    esc = role["esc_key"]
    cases = []
    for pattern, token in role["hook_globs"]:
        cases.append(
            f"""case "$lc_path" in
{pattern})
TOKENS+=("{token}")
;;
esac"""
        )
    case_block = "\n".join(cases)
    w(
        base / ".claude" / "hooks" / "on-stop.sh",
        f"""#!/bin/bash
# Stop hook entry point. Merges agent notes, then rebuilds the trigger index
# when a rules file is newer than facts/trigger-index.json.
INPUT="$(cat 2>/dev/null)"
if command -v jq >/dev/null 2>&1; then
    if [ "$(printf '%s' "$INPUT" | jq -r '.stop_hook_active // false' 2>/dev/null)" = "true" ]; then
        exit 0
    fi
fi
bash "$(dirname "$0")/merge-agent-notes.sh"
WORKSPACE_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
GEN="$WORKSPACE_ROOT/scripts/memory/build_trigger_index.py"
IDX="$WORKSPACE_ROOT/facts/trigger-index.json"
if [ -f "$GEN" ]; then
    stale=0
    if [ ! -f "$IDX" ]; then
        stale=1
    else
        for rf in "$WORKSPACE_ROOT"/facts/rules-{planned}.md \\
                  "$WORKSPACE_ROOT"/facts/rules-{esc}.md; do
            [ -f "$rf" ] && [ "$rf" -nt "$IDX" ] && stale=1 && break
        done
    fi
    if [ "$stale" -eq 1 ]; then
        if command -v python >/dev/null 2>&1; then
            python "$GEN" >/dev/null 2>&1 || true
        elif command -v python3 >/dev/null 2>&1; then
            python3 "$GEN" >/dev/null 2>&1 || true
        fi
    fi
fi
exit 0
""",
    )
    w(
        base / ".claude" / "hooks" / "inject-rules-on-action.sh",
        f"""#!/bin/bash
# PreToolUse hook: inject expert rules that match the action about to happen.
# Triggers are management actions for this expert ({role['title']}).
# stdout: hook JSON with additionalContext. exit: always 0.
INPUT="$(cat 2>/dev/null)"
command -v jq >/dev/null 2>&1 || exit 0
WORKSPACE_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
INDEX="$WORKSPACE_ROOT/facts/trigger-index.json"
[ -f "$INDEX" ] || exit 0
TOOL_NAME="$(printf '%s' "$INPUT" | jq -r '.tool_name // empty' 2>/dev/null)"
FILE_PATH="$(printf '%s' "$INPUT" | jq -r '.tool_input.file_path // empty' 2>/dev/null)"
PATH_NORM="$(printf '%s' "$FILE_PATH" | tr '\\\\' '/')"
TOKENS=()
case "$TOOL_NAME" in
Write|Edit|MultiEdit)
lc_path="$(printf '%s' "$PATH_NORM" | tr '[:upper:]' '[:lower:]')"
{case_block}
case "$lc_path" in
*.md|*.markdown)
TOKENS+=("write:doc")
;;
esac
;;
esac
[ "${{#TOKENS[@]}}" -eq 0 ] && exit 0
UNIQ_TOKENS=()
for t in "${{TOKENS[@]}}"; do
skip=
for u in "${{UNIQ_TOKENS[@]}}"; do
[ "$u" = "$t" ] && skip=1 && break
done
[ -z "$skip" ] && UNIQ_TOKENS+=("$t")
done
TOKENS_JSON="$(printf '%s\\n' "${{UNIQ_TOKENS[@]}}" | jq -R . | jq -s -c .)"
OUTPUT="$(jq -c --argjson toks "$TOKENS_JSON" '
  . as $index
  | [ $toks[] as $t | ($index[$t] // [])[] ]
  | unique_by(.file + "|" + (.line|tostring))
  | if length == 0 then empty
    else
      ("Expert rules for the action you are about to take "
        + "(matched triggers: " + ($toks | join(", ")) + "). "
        + "Follow them:\\n\\n"
        + (map("---\\n" + .body) | join("\\n\\n"))
      ) as $ctx
      | {{ hookSpecificOutput: {{ hookEventName: "PreToolUse", additionalContext: $ctx }} }}
    end
' "$INDEX" 2>/dev/null)"
[ -z "$OUTPUT" ] && exit 0
printf '%s\\n' "$OUTPUT"
exit 0
""",
    )


def emit_claude(role, base: Path):
    p, e = role["planned_key"], role["esc_key"]
    w(
        base / "CLAUDE.md",
        f"""# Management expert

You are the {role['title']} expert. {role['blurb']}

1. **Identity**: You turn a management request into a charter, an operating plan, diagrams, an action list, execution notes, verification, and a close-out. You also continue work already in flight: change requests, escalations, and cleaner ways of working. You grow by remembering facts and rules about this role.

2. **State**: Progress for a work item lives in `work-items/<id>/journal/progress.md`. The role itself lives in `MyRole.txt` and `docs/role/role-definition.md`. At the start of every response, and especially when the operator says "continue" or "start", read `MyRole.txt`. If `Role status` is `pending`, run **define-role** and do not start a work item.

3. **Pipeline**: Planned work (`{p}`): intake, charter, plan, diagrams, action breakdown, kickoff, execute, verify, close-out. Urgent work (`{e}`): assess, analyze impact, respond, monitor, resolve and document. Change requests and ways-of-working improvements follow their own skills. Do not skip a phase unless the journal says it is already complete.

4. **Skills**: Use the skills in `.claude/skills/`. After every phase, follow **journal-keeper**. On first start, follow **define-role**.

5. **Continue**: When the operator says "continue", "start", or "resume", run **continue**. It reads the journal and performs the next step. It is not an answer and not an approval.

6. **Continue does not mean answer or approval**: If the next step is "wait for answer" or "wait for approval", re-prompt. Only a substantive answer, or an explicit phrase such as "I approve the charter", "I approve the plan", "I approve the change", "I approve the response", "I approve the role", or the matching "Skip ..." phrase, clears the wait.

7. **Blocking questions**: Do not proceed past a step that has unanswered blocking questions. Ask them. Record each answer in the same turn.

8. **Templates**: Before the charter or the plan, ask whether the operator has a template to follow. Charter depth is **Standard** (outcome and scope), **Part 1** (plus stakeholders and dependencies), or **Extended** (plus risks, communications, and constraints).

9. **Same-turn record**: When the operator answers, record the question and the answer in the same response, remove it from open questions, and continue or ask the next question.

10. **Human gates**: After the charter and its diagrams are ready, wait for charter approval before the plan. After the plan and its diagrams are ready, wait for plan approval before kickoff. A change request waits for change approval. An escalation waits for response approval before the response is carried out. Record the approval in the journal.

11. **Definition of done**: The work item is done when every action is complete, verification is recorded (or an exception is written), and close-out is written. Do not treat the item as done while a gate is still waiting.

12. **Session summary**: Before the operator stops, write **Last session summary** in the journal and refresh `STATUS.md`: what finished, what is next, and what you need from the operator.

13. **Ways of working**: When a change would duplicate a tracker, a cadence, or a decision, use **improve-ways-of-working**. Do not change the agreed outcome while cleaning that up.

14. **Verification**: Record acceptance, stakeholder sign-off, and the risk review in `docs/verification/verification.md` before close-out.

15. **Notes and memory**: When the operator says "remember this" or brings notes, use **remember** or **integrate-docs**. During role definition, ask for notes they already have from doing this job. People-sensitive notes stay out of expert-role memory unless the operator explicitly says to store them.

16. **Blockers**: When you are blocked, say what is blocked and what you need. Do not invent a workaround. If you need a file, a name, or a decision, ask.

17. **Setup before execution**: Kickoff creates the cadence, the tracker, the decision log, and the stakeholder list from the approved plan before any execute action. Do not start execute actions until that setup exists.

18. **Diagrams**: Charter and plan phases own the diagrams in `docs/diagrams/`. Use **diagram-generator** to rebuild them when the documents change. Diagrams for this role: {", ".join(role["diagrams"])}.

19. **Work item isolation**: If no work item is active, ask for an id such as `WID-21411151`, but only after role status is `defined` or `skipped`. State for a work item lives in `work-items/<id>/`. Role, skills, and expert memory stay at the top level: `CLAUDE.md`, `.claude/skills/`, `facts/`, `MyRole.txt`. The active id is `.claude/active-context.txt` (`work-item:WID-...`). `.claude/active-work-item.txt` is the legacy pointer.

20. **Role-aware pipelines**: Read `MyRole.txt` for the role and the pipelines. **{role['planned_name']}** is the planned pipeline. **{role['esc_name']}** is the urgent pipeline. A third pipeline exists only after define-role approves one. **workflow-selector** offers only the workflows still enabled.

21. **Facts and rules**: Facts inform. Rules constrain. Work-item memory is `work-items/<id>/facts/`. Expert-role memory is `facts/facts-{p}.md`, `facts/rules-{p}.md`, `facts/facts-{e}.md`, and `facts/rules-{e}.md`. Load the pair that matches the work item's workflow. Follow every loaded rule.

22. **Proactive detection**: When you notice a repeated management pattern, propose it: "This seems like a new rule for your role. Should I remember this?" Capture it only if the operator agrees.

23. **Promotion**: At the end of a work item, or when asked, use **promote-facts-rules**. Do not promote people-sensitive notes unless the operator says yes.

Prefer finishing one pipeline step and updating the journal over starting many steps.

Tell the operator if you need them to provide a note, a decision, or a stakeholder name before you can continue.
""",
    )


def emit_myrole(role, base: Path):
    w(
        base / "MyRole.txt",
        f"""# My Role Definition

**Role status:** pending

**Role title:** {role['title']}

**Who this expert serves:** [Filled when the operator completes define-role]

**Responsibilities:**
{ul(role["responsibilities"])}

**Decision rights:** [Filled when the operator completes define-role]

**Out of scope:** {role["never"]}

---

# Primary Workflows (Pipelines)

## Pipeline 1: {role['planned_name']}

**Workflow key:** {role['planned_key']}

**When to use:** {role['when_planned']}

**Phases:** intake → charter-writer → plan-writer → diagram-generator → action-breakdown → kickoff → execute-action → verify → close-out

**Human gates:**
- Charter approval after the {role['charter_title'].lower()} and its diagrams ("I approve the charter" or "Skip charter approval")
- Plan approval after the {role['plan_title'].lower()} and its diagrams ("I approve the plan" or "Skip plan approval")
- Change approval before a change request is applied ("I approve the change" or "Skip change approval")

**Characteristics:**
- {role['charter_title']} sections: {", ".join(role["charter_sections"])}
- {role['plan_title']} sections: {", ".join(role["plan_sections"])}
- Diagrams: {", ".join(role["diagrams"])}
- Verification: {", ".join(role["verify"])}

---

## Pipeline 2: {role['esc_name']}

**Workflow key:** {role['esc_key']}

**When to use:** {role['when_esc']}

**Phases:** assess-situation → analyze-impact → respond → monitor-situation → resolve-and-document

**Human gates:**
- Response approval before the response is carried out ("I approve the response" or "Skip response approval")

**Characteristics:**
- {role['esc_focus']}
- No charter or plan phase

---

## Pipeline 3: Custom pipeline

**When to use:** Only after define-role agrees that a recurring workflow is missing. Examples of what might appear later: {role['custom_examples']}

**Phases:** [Defined with the operator during define-role]

**Human gates:** [Defined with the operator during define-role]

**Characteristics:** Not enabled until "I approve the role" writes it into the workflow registry.

---

# Pipeline Selection Guidance

- **{role['planned_name']}:** {role['when_planned']}
- **{role['esc_name']}:** {role['when_esc']}
- **Custom:** Leave unused until define-role approves a third pipeline.

---

# Notes

This file starts from the {role['title']} starter pack. define-role rewrites the title, responsibilities, decision rights, workflows, and skills when the operator says "I approve the role". "Skip role definition" leaves this starter pack in place and sets Role status to skipped.
""",
    )


def emit_quickstart(role, base: Path):
    qs = "\n".join(f"{i}. {q}" for i, q in enumerate(role["intake_questions"], 1))
    ans = "\n".join(f"{i}. {a}" for i, a in enumerate(role["quick_answers"], 1))
    w(
        base / "QUICK-START.md",
        f"""# Quick Start Guide

## What This Is

An expert system for a {role['title']}. It turns a management request into a {role['charter_title'].lower()}, a {role['plan_title'].lower()}, diagrams, actions, verification, and a close-out. All work-item state lives in a Work Item (`WID-…`). The role itself is defined before the first work item.

## Getting Started

Open this folder and say **"start"**, **"continue"**, or **"define my role"**.

1. If `MyRole.txt` says `Role status: pending`, the define-role skill asks about the specific job, the workflows, the skills, and any notes you already have from doing this work without an AI expert.
2. "Continue" does not answer those questions and does not approve the role.
3. After you say "I approve the role" (or "Skip role definition"), say **start** again and give a Work Item id such as `WID-21411151`.
4. Choose **{role['planned_name']}** or **{role['esc_name']}**.
5. The journal's next action is the only step that runs.

## Planned pipeline

`intake → charter-writer → plan-writer → diagram-generator → action-breakdown → kickoff → execute-action → verify → close-out → done`

## Urgent pipeline

`assess-situation → analyze-impact → respond → monitor-situation → resolve-and-document → done`

## Human gates

- Charter: "I approve the charter" or "Skip charter approval"
- Plan: "I approve the plan" or "Skip plan approval"
- Change: "I approve the change" or "Skip change approval"
- Escalation response: "I approve the response" or "Skip response approval"
- Role: "I approve the role" or "Skip role definition"

## What you can say

| What you say | What happens |
| --- | --- |
| "start" / "continue" / "resume" | Next step in the journal, or role definition if the role is pending |
| "define my role" | Run role onboarding again |
| "switch to work item WID-…" | Point later steps at that work item |
| "I approve the charter" | Clear the charter gate |
| "I approve the plan" | Clear the plan gate |
| "remember this …" | Store a fact or a rule |
| "integrate this …" | Fold a document into facts, rules, and MyRole.txt |
| "promote facts/rules" | Review work-item learnings for expert-role memory |
| "change request" | Start a change for {role['change_kind']} |
| "improve ways of working" | Clean up cadence, trackers, or decision hygiene |

## Example

```
You: start
Agent: Role status is pending. I will define the {role['title']} role before any work item.

       What is your exact title, and who does this role serve?
You: [your answer]
Agent: [records it and asks the next question, including notes you already have]

You: I approve the role
Agent: What are you working on? (work item WID-XXXXXXXX)
You: WID-21411151
Agent: Which workflow applies?
       1. {role['planned_name']}
       2. {role['esc_name']}
You: 1

       Blocking questions:
{qs}
You:
{ans}
Agent: [records the answers]
       [writes the {role['charter_title'].lower()} after you choose a depth]
       Charter is ready. Reply "I approve the charter" to proceed.
```

## Learn more

- `CLAUDE.md` — operating rules
- `MyRole.txt` — role and pipelines
- `.claude/workflows/{role['planned_key']}.md` — planned phases
- `.claude/workflows/{role['esc_key']}.md` — urgent phases
- `docs/manager-operating-system.md` — longer description
""",
    )


def emit_workflows(role, base: Path):
    p, e = role["planned_key"], role["esc_key"]
    registry = {
        "workflows": {
            p: {
                "name": role["planned_name"],
                "description": role["when_planned"],
                "instruction_file": f".claude/workflows/{p}.md",
                "initial_phase": "intake",
            },
            e: {
                "name": role["esc_name"],
                "description": role["when_esc"],
                "instruction_file": f".claude/workflows/{e}.md",
                "initial_phase": "assess-situation",
            },
        }
    }
    w(base / ".claude" / "workflows" / "workflow-registry.json", json.dumps(registry, indent=2))
    w(
        base / ".claude" / "workflows" / f"{p}.md",
        f"""# {role['planned_name']}

**When to use:** {role['when_planned']}

## Phase Sequence

intake → charter-writer → plan-writer → diagram-generator → action-breakdown → kickoff → execute-action (loop) → verify → close-out → done

## Approval Gates

- **Charter approval** after the {role['charter_title'].lower()} and diagrams: "I approve the charter" or "Skip charter approval"
- **Plan approval** after the {role['plan_title'].lower()} and diagrams: "I approve the plan" or "Skip plan approval"
- **Change approval** for change-request: "I approve the change" or "Skip change approval"

## Artifact Organization

- Brief: `work-items/<id>/docs/charter/brief.md`
- {role['charter_title']}: `work-items/<id>/docs/charter/charter.md`
- {role['plan_title']}: `work-items/<id>/docs/plan/operating-plan.md`
- Diagrams: `work-items/<id>/docs/diagrams/*.mmd` and `index.html`
- Decision log: `work-items/<id>/docs/decisions/decision-log.md`
- Actions: `work-items/<id>/TODOS.md`
- Changes: `work-items/<id>/docs/changes/<change-id>/`
- Verification: `work-items/<id>/docs/verification/verification.md`

## Phase Behaviors

### intake

- Write `docs/charter/brief.md`
- Ask: {"; ".join(role["intake_questions"])}
- Set next action: "run charter-writer"

### charter-writer

- Ask charter depth: Standard, Part 1, or Extended
- Write `docs/charter/charter.md` titled **{role['charter_title']}** with sections: {", ".join(role["charter_sections"])}
- Draft the diagrams listed below
- Set next action: "wait for charter approval"

### plan-writer

- Write `docs/plan/operating-plan.md` titled **{role['plan_title']}** with sections: {", ".join(role["plan_sections"])}
- Update diagrams
- Set next action: "wait for plan approval"

### diagram-generator

- Write one Mermaid file per diagram: {", ".join(role["diagrams"])}
- Refresh `docs/diagrams/index.html`
- Set next action: "run action-breakdown"

### action-breakdown

- Write `TODOS.md` with sections: Setup, Dependencies and asks, Kickoff, Execution, Verification, Communication and close-out
- Order setup and kickoff before execution
- Set next action: "run kickoff"

### kickoff

- Create: {", ".join(role["kickoff"])}
- Set next action: "execute-action (task 1/N)"

### execute-action

- Complete one TODO. Outputs include: {", ".join(role["execute"])}
- {role["never"]}
- Set next action to the next task, or "run verify" when the list is finished

### verify

- Write `docs/verification/verification.md` covering: {", ".join(role["verify"])}
- Set next action: "run close-out"

### close-out

- Write the close-out: {role["close_out"]}
- Record the status narrative, the decision-log path, and the handoff note in the journal
- Set next action: "done"
""",
    )
    w(
        base / ".claude" / "workflows" / f"{e}.md",
        f"""# {role['esc_name']}

**When to use:** {role['when_esc']}

## Phase Sequence

assess-situation → analyze-impact → respond → monitor-situation → resolve-and-document → done

## Approval Gates

- **Response approval** after impact analysis: "I approve the response" or "Skip response approval"

## Artifact Organization

- `work-items/<id>/docs/escalations/assessment.md`
- `work-items/<id>/docs/escalations/impact.md`
- `work-items/<id>/docs/escalations/response.md`
- `work-items/<id>/docs/escalations/monitor.md`
- `work-items/<id>/docs/escalations/resolution.md`

## Phase Behaviors

### assess-situation

- Write `docs/escalations/assessment.md`
- Cover: {role['esc_focus']}
- Set next action: "run analyze-impact"

### analyze-impact

- Write `docs/escalations/impact.md` with options and who decides
- Set next action: "wait for response approval"

### respond

- Write `docs/escalations/response.md` and carry out only the approved response
- Set next action: "run monitor-situation"

### monitor-situation

- Write what is being watched and the next check into `docs/escalations/monitor.md`
- Set next action: "run resolve-and-document"

### resolve-and-document

- Write `docs/escalations/resolution.md` as a management record of what was decided, what was communicated, and what remains open
- Set next action: "done"
""",
    )
    w(
        base / ".claude" / "workflows" / "README.md",
        f"""# Workflow Framework

Workflows are registered in `workflow-registry.json`. Each work item stores `Workflow type` in its journal. continue loads the matching instruction file.

## Available Workflows

1. **{role['planned_name']}** (`{p}`)
   - {role['when_planned']}
   - Gates: charter approval, plan approval
   - Artifacts: `docs/charter/`, `docs/plan/`, `docs/diagrams/`, `TODOS.md`, `docs/verification/`

2. **{role['esc_name']}** (`{e}`)
   - {role['when_esc']}
   - Gate: response approval
   - Artifacts: `docs/escalations/`

define-role may disable one of these or approve a third pipeline. workflow-selector offers only workflows still listed in the registry.

## How a work item runs

1. continue reads `Workflow type` from the journal. If it is missing, workflow-selector asks the operator to choose.
2. The instruction file supplies the phase order, the gates, and the artifact paths.
3. journal-keeper records the phase, the artifacts, and the next action.

## Adding a workflow

Do this only from define-role, after the operator approves the role:

1. Add the workflow to `workflow-registry.json` with `name`, `description`, `instruction_file`, and `initial_phase`.
2. Create `.claude/workflows/<key>.md` with the phase sequence, gates, artifacts, and phase behaviors.
3. Point the new phases at skills that already exist, or describe the new skill in `.claude/role-skills.md` and add the skill folder in the same turn the operator approved it.
""",
    )


def emit_context_and_docs(role, base: Path):
    w(
        base / ".claude" / "CONTEXT-SYSTEM.md",
        f"""# Active context

`.claude/active-context.txt` stores `<type>:<id>`. Today the type is `work-item`.

| Type | Example | Purpose |
| --- | --- | --- |
| work-item | `work-item:WID-21411151` | Management work for this {role['title']} expert: planned initiatives and escalations |

`.claude/active-work-item.txt` stores the same id for older skills.

Workflows for a work item: `{role['planned_key']}`, `{role['esc_key']}`.

Role onboarding is not a work item. It writes `docs/role/role-definition.md` and updates `MyRole.txt`.
""",
    )
    w(
        base / "docs" / "manager-operating-system.md",
        f"""# {role['title']} operating system

This expert supports one manager type. The folder is the type. define-role specializes the job, the workflows, and the skills. Facts and rules accumulate after that.

## Planned work

{role['when_planned']}

Phases: intake, charter-writer, plan-writer, diagram-generator, action-breakdown, kickoff, execute-action, verify, close-out.

The charter document is titled **{role['charter_title']}** and is stored at `docs/charter/charter.md`. The plan document is titled **{role['plan_title']}** and is stored at `docs/plan/operating-plan.md`.

Charter sections: {", ".join(role["charter_sections"])}.

Plan sections: {", ".join(role["plan_sections"])}.

Diagrams: {", ".join(role["diagrams"])}.

Execute actions produce: {", ".join(role["execute"])}.

Verification checks: {", ".join(role["verify"])}.

Close-out: {role['close_out']}

## Urgent work

{role['when_esc']}

{role['esc_focus']}

## Change request

Use change-request for {role['change_kind']}. Approval is required before the plan is edited.

## Ways of working

improve-ways-of-working cleans cadence, trackers, and decision hygiene without changing the agreed outcome.

## Memory

Load `facts/facts-{role['planned_key']}.md` and `facts/rules-{role['planned_key']}.md` for planned work. Load `facts/facts-{role['esc_key']}.md` and `facts/rules-{role['esc_key']}.md` for urgent work. `facts/MEMORY-INDEX.md` is the map.

## Role onboarding

define-role asks for the specific title, accountability, decision rights, a normal week, which workflows and skills apply, and any notes the operator already has. Confirmed notes become facts and rules. People-sensitive notes are stored in expert-role memory only when the operator says so.
""",
    )


def emit_memory(role, base: Path):
    p, e = role["planned_key"], role["esc_key"]
    facts_p = "\n".join(mem_fact(role, f) for f in role["facts"] if f["workflows"] == "planned")
    facts_e = "\n".join(mem_fact(role, f) for f in role["facts"] if f["workflows"] == "esc")
    rules_p = "\n".join(mem_rule(role, r) for r in role["rules"] if r["workflows"] == "planned")
    rules_e = "\n".join(mem_rule(role, r) for r in role["rules"] if r["workflows"] == "esc")
    w(base / "facts" / f"facts-{p}.md", f"# Facts: {role['planned_name']}\n\n{facts_p}")
    w(base / "facts" / f"facts-{e}.md", f"# Facts: {role['esc_name']}\n\n{facts_e}")
    w(base / "facts" / f"rules-{p}.md", f"# Rules: {role['planned_name']}\n\n{rules_p}")
    w(base / "facts" / f"rules-{e}.md", f"# Rules: {role['esc_name']}\n\n{rules_e}")
    triggers = ", ".join(f"`{t}`" for t in role["triggers"])
    w(
        base / "facts" / "MEMORY-INDEX.md",
        f"""# Memory System Index

Load this index first, then only the workflow pair you need.

## Two axes

1. **Workflow axis** (this file). Load `facts-<workflow>.md` and `rules-<workflow>.md` for the session.
2. **Trigger axis** (`TRIGGER-INDEX.md`, generated). Rules carry `**Triggers:**`. The hook `.claude/hooks/inject-rules-on-action.sh` injects a matching rule when that action happens.

Regenerate the trigger index with `python scripts/memory/build_trigger_index.py` after retagging a rule. Do not hand-edit `TRIGGER-INDEX.md` or `trigger-index.json`.

## {role['planned_name']}

**When to use:** {role['when_planned']}

- [facts-{p}.md](facts-{p}.md)
- [rules-{p}.md](rules-{p}.md)

## {role['esc_name']}

**When to use:** {role['when_esc']}

- [facts-{e}.md](facts-{e}.md)
- [rules-{e}.md](rules-{e}.md)

Default workflow when a session is ambiguous: `{p}`.

Starter triggers: {triggers}.

## Fact entry

```markdown
### year-month-day: Descriptive Title

**Scope:** expert-role

**Workflows:** {p} | {e} | all

**Captured:** year-month-day

**Source:** where this came from

What is true, and why it matters for this role.
```

## Rule entry

```markdown
### year-month-day: Prescriptive Title

**Scope:** expert-role

**Workflows:** {p} | {e} | all

**Triggers:** {" | ".join(role["triggers"])} | none

**Captured:** year-month-day

**Source:** where this came from

**Rule:** What must be done

**Why:** Why it matters

**How to apply:** What to do when it applies
```
""",
    )
    w(
        base / "facts" / "HOW-MEMORY-LOADING-WORKS.md",
        f"""# How memory loading works

1. Read `facts/MEMORY-INDEX.md`.
2. Read `Workflow type` from the work-item journal.
3. Load only the matching pair:
   - `{p}` → `facts-{p}.md` and `rules-{p}.md`
   - `{e}` → `facts-{e}.md` and `rules-{e}.md`
4. Also load `work-items/<id>/facts/facts.md` and `rules.md` with no workflow filter.
5. Drop an expert-role entry whose `Workflows` list does not include the current workflow or `all`.
6. Follow every loaded rule. Use facts as context.
7. Log the counts in the journal.

If the workflow is missing, default to `{p}`.

People-sensitive notes are not expert-role memory unless the operator explicitly said to store them.

The action hook reads `facts/trigger-index.json` and can surface a rule during any workflow when its trigger matches.
""",
    )


def emit_template(role, base: Path):
    root = base / "work-items" / "_TEMPLATE"
    w(root / "journal" / "progress.md", "Project progress\n")
    w(
        root / "STATUS.md",
        """# Work Item Status

Work Item ID: [WID-XXXXXXXX]
Description: [Brief description]
Pipeline: [pipeline-name]
Current Phase: [phase-name]
Last Updated: [year-month-day HH:MM]

## Last Session Summary

[What was completed, what is next, what is needed from the operator]

## Quick Links

- Journal
- Charter
- Plan
- Diagrams
- Decisions
- Verification
- TODOS
- Work Item Facts
- Work Item Rules

## Recent Activity

- [year-month-day] [Activity]

## Next Action

[Specific next step from the journal]
""",
    )
    w(
        root / "TODOS.md",
        f"""# TODO List

[Generated by action-breakdown from the approved plan]

Work Item: [WID-XXXXXXXX]
Pipeline: [pipeline-name]

## Setup

[Cadence, tracker, decision log, and stakeholder list. These come first.]

## Dependencies and asks

[Decisions, names, or inputs the operator must supply]

## Kickoff

{ul(role["kickoff"])}

## Execution

{ul(role["execute"])}

## Verification

{ul(role["verify"])}

## Communication and close-out

[Status narrative, decision log, handoff]

---

Status: [Not started | In progress (task X/N) | Complete]
""",
    )
    w(
        root / "facts" / "facts.md",
        f"""# Work Item Facts

Facts are observations for this work item. They inform the charter, the plan, and the actions. They are not rules.

### year-month-day: [Label]

**Scope:** work-item

**Captured:** year-month-day

**Source:** [optional]

**Status:** [active | promoted-to-expert | archived]

[Content]

Work-item facts do not need `**Workflows:**`. They inherit the work item's workflow.

Expert-role facts use `**Workflows:**` `{role['planned_key']}`, `{role['esc_key']}`, or `all`, and live under `facts/`.
""",
    )
    w(
        root / "facts" / "rules.md",
        f"""# Work Item Rules

Rules constrain this work item. Log a violation in the journal.

### year-month-day: [Label]

**Scope:** work-item

**Captured:** year-month-day

**Source:** [optional]

**Status:** [active | promoted-to-expert | archived]

**Rule:** [statement]

**Why:** [reason]

**How to apply:** [what to do]

Work-item rules do not need `**Workflows:**`.

Expert-role rules live under `facts/rules-{role['planned_key']}.md` or `facts/rules-{role['esc_key']}.md` and include `**Workflows:**` and `**Triggers:**`.
""",
    )


def emit_system_skills(role, base: Path):
    skills = base / ".claude" / "skills"
    p, e = role["planned_key"], role["esc_key"]
    pn, en = role["planned_name"], role["esc_name"]
    questions = "\n".join(f"   - {q}" for q in [
        "What is your exact title, and who does this role serve?",
        "What is this role accountable for?",
        "Which decisions can this role make, and which must someone else approve?",
        "What does a normal week include?",
        "Which starter workflows match that week, and what recurring work do they miss?",
        "Which starter skills are required, and which must this expert not use?",
        "What must this expert never do?",
        *role["extra_questions"],
    ])
    w(
        skills / "define-role" / "SKILL.md",
        skill(
            "define-role",
            "Use when the operator says define my role, or when MyRole.txt says Role status: pending. Asks for the specific job, workflows, skills, and existing notes, then waits for approval.",
            'User says "define my role", or Role status is pending',
            f"""# Define role

Specializes this {role['title']} expert. The folder stays this manager type. The answers define the specific job.

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

{questions}
- Notes: ask for file paths, pasted text, or both. Examples for this role: {role['note_examples']}. Accept further batches until the operator says the notes are complete.

## After the notes

1. For each batch, follow integrate-docs and remember. Classify each item as a fact or a rule. Assign `{p}`, `{e}`, or both. Show the proposed entries and store only the ones the operator confirms.
2. If a note implies a workflow or skill the starter pack does not have, put that proposal in the draft. Do not add it to the registry yet.
3. Draft `docs/role/role-definition.md` with: title, who the role serves, responsibilities, decision rights, out of scope, workflows, skills required for each workflow, skills not used, and the list of remembered notes.
4. A missing recurring workflow is drafted as a third pipeline: when to use, phases, gates, artifacts, and skills.
5. Ask the operator to reply "I approve the role" or to correct the draft. "Skip role definition" keeps the starter pack, leaves confirmed note entries in place, and sets `Role status: skipped`.

## On approval

- Rewrite `MyRole.txt` from the draft and set `Role status: defined`.
- Update `.claude/workflows/workflow-registry.json` so only approved workflows remain. Add a third workflow file only if the draft included one and the operator approved it.
- Write `.claude/role-skills.md` with each skill marked required or not used. Do not delete a skill marked not used.
- Keep the questions, answers, and note sources in `docs/role/role-definition.md`.
""",
        ),
    )
    w(
        skills / "continue" / "SKILL.md",
        skill(
            "continue",
            "Use when the operator says continue, start, or resume. Runs define-role while the role is pending, then performs the next journal step. Continue is not an answer and not an approval.",
            'User says "continue", "start", or "resume"',
            f"""# Continue

## When to use

The operator says "continue", "start", or "resume", or asks to pick up the work.

## Role gate

1. Read `MyRole.txt`.
2. If the operator said "define my role", run define-role and stop.
3. If `Role status` is `pending` or missing, run define-role and stop. Do not ask for a work item.
4. If status is `defined` or `skipped`, continue below.

## Context

5. Read `.claude/active-context.txt` (`work-item:WID-...`). If missing, read `.claude/active-work-item.txt`.
6. If nothing is active, ask: "What are you working on? (work item WID-XXXXXXXX)". Write `.claude/active-context.txt` and `.claude/active-work-item.txt`.
7. Paths: `work-items/<id>/` and `work-items/<id>/journal/progress.md`.
8. If the folder does not exist, copy `work-items/_TEMPLATE/`.
9. If the journal has no `Workflow type`, run workflow-selector, then reload the journal.
10. Load `facts/MEMORY-INDEX.md`, then the pair for that workflow: `facts/facts-{p}.md` and `facts/rules-{p}.md`, or `facts/facts-{e}.md` and `facts/rules-{e}.md`. Then load the work-item facts and rules. Follow the rules. Log the counts.

## This step only

11. If a blocking question is open, ask it again. Continue is not an answer. When a real answer arrives, record it in the same turn.
12. If a blocker is set, describe it and wait for agreement on how to proceed.
13. If the next action is a wait, re-prompt with the file path and the exact phrase. Do not advance. Phrases: "I approve the charter" or "Skip charter approval"; "I approve the plan" or "Skip plan approval"; "I approve the change" or "Skip change approval"; "I approve the response" or "Skip response approval"; "I approve the role" or "Skip role definition".
14. If the next action is empty or "done", stop and ask what to do next.
15. Otherwise run the single next step:

**{pn} (`{p}`):**

- "run intake" → `docs/charter/brief.md`, then "run charter-writer"
- "run charter-writer" → `docs/charter/charter.md` titled {role['charter_title']}, diagrams, then "wait for charter approval"
- "run plan-writer" → `docs/plan/operating-plan.md` titled {role['plan_title']}, then "wait for plan approval"
- "run diagram-generator" → `docs/diagrams/`, then "run action-breakdown"
- "run action-breakdown" → `TODOS.md`, then "run kickoff"
- "run kickoff" → cadence, tracker, decision log, stakeholder list, then "execute-action (task 1/N)"
- "execute-action (task K/N)" → one TODO, then the next task or "run verify"
- "run verify" → `docs/verification/verification.md`, then "run close-out"
- "run close-out" → status narrative, decision log, handoff, then "done"
- "run change-request" → `docs/changes/<change-id>/`, then "wait for change approval"
- "run improve-ways-of-working" → clean cadence or trackers without changing the outcome

**{en} (`{e}`):**

- "run assess-situation" → `docs/escalations/assessment.md`
- "run analyze-impact" → `docs/escalations/impact.md`, then "wait for response approval"
- "run respond" → `docs/escalations/response.md`
- "run monitor-situation" → `docs/escalations/monitor.md`
- "run resolve-and-document" → `docs/escalations/resolution.md`, then "done"

16. Update the journal (journal-keeper): phase, artifacts, next action, facts and rules loaded.
17. At session end, write Last session summary and refresh STATUS.md.
18. When the work item is done, ask whether to promote facts and rules.

Do not skip a phase the journal still has open. Do not run a skill marked not used in `.claude/role-skills.md` when that file exists.
""",
        ),
    )
    w(
        skills / "journal-keeper" / "SKILL.md",
        skill(
            "journal-keeper",
            "Use after every pipeline phase or when the operator answers a question. Updates the work-item journal and STATUS.",
            "After every phase or when the operator answers",
            f"""# Journal keeper

Journal: `work-items/<id>/journal/progress.md`. Status: `work-items/<id>/STATUS.md`. Active id: `.claude/active-work-item.txt`.

## Fields to keep

- Work Item ID, description
- Workflow type: `{p}` or `{e}` (set once by workflow-selector)
- Pipeline phases
- External references
- Mode: planned | change-request
- Current phase: intake | charter | plan | diagrams | actions | kickoff | execution | verify | close-out | escalation | done
- Current change id, when a change request is open
- Last completed, Next action
- Artifacts (paths relative to the work item)
- Facts and rules loaded, conflicts, and proposals
- Open questions (blocking and deferred)
- Resolved Q&A with the date
- Blockers and last failure
- Completion status and last session summary
- Charter depth: standard | part1 | extended

Do not store a repo URL, a branch name, or a commit strategy. Close-out stores the status narrative, the decision-log path, and the handoff note instead.

## After each phase

1. Set Last completed.
2. Append artifacts.
3. Set Next action from the workflow file.
4. Update the facts and rules counts.
5. Leave the phase incomplete while a blocking question is open.
6. Do not change Workflow type.

## When the operator answers

In the same response, append the date, the question, and the answer under Resolved Q&A and remove the question from the open list.

## Session end

Write Last session summary: what finished, what is next, what you need. Refresh STATUS.md quick links: Journal, Charter, Plan, Diagrams, Decisions, Verification, TODOS, Facts, Rules.
""",
        ),
    )
    w(
        skills / "workflow-selector" / "SKILL.md",
        skill(
            "workflow-selector",
            "Use when the journal has no workflow type. Offers only the workflows enabled for this role.",
            "Journal is missing Workflow type",
            f"""# Workflow selector

1. Read `.claude/workflows/workflow-registry.json`. Offer only those workflows. If `.claude/role-skills.md` exists, do not offer a workflow the role definition disabled.
2. Ask which workflow applies:

   1. {pn} — {role['when_planned']}
   2. {en} — {role['when_esc']}

   Include a third line only when the registry contains one.
3. Accept a number or a name. If the choice is not in the registry, ask again.
4. Ask for any external references (notes, tickets, decision threads).
5. For `{e}`, also ask: who is affected, and what decision is needed now?
6. Write the journal: `Workflow type`, context id, initial phase, and next action (`run intake` for `{p}`, `run assess-situation` for `{e}`).
7. Confirm the workflow name, the initial phase, and the next action.
""",
        ),
    )
    w(
        skills / "switch-context" / "SKILL.md",
        skill(
            "switch-context",
            "Use when the operator says switch to work item WID-XXXXXXXX. Points later steps at that work item.",
            'User says "switch to work item WID-..."',
            """# Switch context

1. Parse the WID. If the folder does not exist, copy `work-items/_TEMPLATE/`, then run workflow-selector.
2. Confirm the switch with the operator.
3. Write `.claude/active-context.txt` as `work-item:<WID>` and the same id to `.claude/active-work-item.txt`.
4. Show workflow type, current phase, next action, and any open question or gate.
5. Offer "continue" as the way to take the next step. Do not take it in this turn unless the operator already asked you to continue.
""",
        ),
    )
    w(
        skills / "remember" / "SKILL.md",
        skill(
            "remember",
            "Use when the operator says remember this, or when a reusable management fact or rule appears. Classifies and stores it.",
            'User says "remember this" or a new rule is detected',
            f"""# Remember

## When to use

The operator says "remember this", "note this down", "save this", or you detect a repeated pattern and they agree to store it.

## Steps

1. If they did not already say, ask whether it is a **fact** (what is true) or a **rule** (what must be done), and whether it is **work-item** or **expert-role**.
2. Expert-role entries need `Workflows`: `{p}`, `{e}`, `all`, or a comma-separated list. Ask if it is unclear. Also ask for `Triggers` on a rule. Use `none` when no action should surface it. Starter triggers include: {", ".join(role["triggers"])}.
3. People-sensitive material (private conversations, performance, personal circumstances) is not stored in expert-role memory unless the operator explicitly says to store it. Offer to keep it on the work item instead.
4. Show the entry, then write it.
   - Work item: `work-items/<id>/facts/facts.md` or `rules.md`
   - Expert role: `facts/facts-<workflow>.md` or `facts/rules-<workflow>.md`
5. Use the entry shape in `facts/MEMORY-INDEX.md`. Check for a duplicate first.
6. Confirm what was stored and where. Mention regenerating the trigger index when a rule's triggers changed: `python scripts/memory/build_trigger_index.py`.
7. Record the capture in the journal under proactively detected facts and rules, when a work item is active.

## Proactive detection

During intake, charter, plan, execute, change-request, or escalation, if the operator states a constraint you would reuse, propose the fact or rule and its scope. Store it only after they agree.
""",
        ),
    )
    w(
        skills / "integrate-docs" / "SKILL.md",
        skill(
            "integrate-docs",
            "Use when the operator provides notes, exports, or write-ups to fold into facts, rules, and MyRole.txt.",
            "User provides notes or says integrate this",
            f"""# Integrate documents

Use this when define-role collects existing notes, and whenever the operator supplies a file or pasted text to remember.

## Steps

1. Ask for file paths, pasted text, or both, plus an optional hint about the topic. "I have no notes" means stop.
2. Read every path. Split the material into facts and rules.
   - Facts: who decides, cadence, stakeholders, historical outcomes, where trackers live.
   - Rules: how status is written, how a decision is recorded, what must be approved, who must be told.
3. Assign each entry to `{p}`, `{e}`, or both. Set triggers from: {", ".join(role["triggers"])}.
4. Hold back people-sensitive notes unless the operator explicitly says to store them in expert-role memory.
5. Show the proposed entries. Store only confirmed ones in the matching `facts/facts-*.md` or `facts/rules-*.md` files.
6. If a note describes a recurring workflow the registry does not have, propose it for MyRole.txt and, during define-role, put it in the role draft. Do not enable it before approval.
7. Update `facts/MEMORY-INDEX.md` when a new topic needs a pointer.
8. Summarize what was stored, what was skipped, and which files changed. Regenerate the trigger index when rules changed.
""",
        ),
    )
    w(
        skills / "promote-facts-rules" / "SKILL.md",
        skill(
            "promote-facts-rules",
            "Use when a work item is done or the operator asks to promote facts and rules into expert-role memory.",
            "Work item is done, or user asks to promote facts/rules",
            f"""# Promote facts and rules

1. Read `work-items/<id>/facts/facts.md` and `rules.md`. List entries whose status is still active.
2. Ask, one group at a time, which entries to promote. Skip people-sensitive notes unless the operator explicitly says to promote them.
3. Generalize wording that only makes sense for this one work item.
4. Write promoted entries into `facts/facts-{p}.md` or `facts/rules-{p}.md` (or the `{e}` pair when that was the workflow), with `Workflows` and, for rules, `Triggers`.
5. Mark the work-item copy `promoted-to-expert`.
6. Record the promotions in the journal.
7. If the work item used a cadence the registry does not name, ask whether to add a pipeline to MyRole.txt. Add it only after they agree, and add the workflow file and registry entry in that same turn.
8. Remind the operator that expert-role files changed, and regenerate the trigger index when a rule moved.
""",
        ),
    )
    w(
        skills / "memory-optimize" / "SKILL.md",
        skill(
            "memory-optimize",
            "Use when the operator asks to check or clean expert memory. Runs analyze-memory.py against this role's fact and rule files.",
            "User asks to optimize or check expert memory",
            f"""# Memory optimize

Files in scope:

- `facts/facts-{p}.md`
- `facts/rules-{p}.md`
- `facts/facts-{e}.md`
- `facts/rules-{e}.md`
- `facts/MEMORY-INDEX.md`

## Steps

1. Run `python .claude/skills/memory-optimize/scripts/analyze-memory.py` from this expert's folder (or the script path under `.claude/skills/memory-optimize/scripts/`).
2. Report file size, entry counts, missing `Workflows` or `Triggers`, and duplicate titles.
3. Thresholds: under 1500 lines per file is healthy. A missing trigger on a rule is a warning. A duplicate title across files needs a look.
4. Propose a short plan before editing: fix metadata, merge true duplicates, refresh MEMORY-INDEX.
5. Edit only after the operator agrees. Do not drop a people-sensitive holdback. Regenerate `python scripts/memory/build_trigger_index.py` after trigger edits.
""",
        ),
    )


def emit_domain_skills(role, base: Path):
    skills = base / ".claude" / "skills"
    charter_sections = ", ".join(role["charter_sections"])
    plan_sections = ", ".join(role["plan_sections"])
    diagrams = ", ".join(role["diagrams"])
    questions = "\n".join(f"- {q}" for q in role["intake_questions"])
    w(
        skills / "intake" / "SKILL.md",
        skill(
            "intake",
            "Use when the next action is run intake. Writes the brief and raises blocking questions.",
            'Next action is "run intake"',
            f"""# Intake

Load work-item and expert-role facts and rules before writing.

1. Read the journal and any brief the operator pointed at.
2. Ask these questions if the answers are not already in Resolved Q&A. They are blocking:

{questions}

3. The word continue is not an answer. Record each answer in the same turn.
4. Write `work-items/<id>/docs/charter/brief.md` with the answers, the unknowns, and the risks.
5. Set next action to "run charter-writer".
6. Update the journal.
""",
        ),
    )
    w(
        skills / "charter-writer" / "SKILL.md",
        skill(
            "charter-writer",
            "Use when the next action is run charter-writer. Writes the charter and asks for approval.",
            'Next action is "run charter-writer"',
            f"""# Charter writer

1. Ask whether the operator has a template. If not, ask charter depth:
   - **Standard** — outcome and scope
   - **Part 1** — Standard, plus stakeholders and dependencies
   - **Extended** — Part 1, plus risks, communications, and constraints
2. Write `docs/charter/charter.md`. The document title is **{role['charter_title']}**. Sections: {charter_sections}.
3. Apply expert-role rules. Do not invent a decision the operator has not made.
4. Draft Mermaid diagrams for: {diagrams}. Write them under `docs/diagrams/` and refresh `index.html`.
5. Set next action to "wait for charter approval". Tell the operator the path and that the reply must be "I approve the charter" or "Skip charter approval".
6. Update the journal, including charter depth.
""",
        ),
    )
    w(
        skills / "plan-writer" / "SKILL.md",
        skill(
            "plan-writer",
            "Use when the next action is run plan-writer, after the charter is approved.",
            'Next action is "run plan-writer"',
            f"""# Plan writer

1. Read the approved charter and the brief. If charter approval is not recorded, stop and return to the gate.
2. Ask whether the operator has a plan template.
3. Write `docs/plan/operating-plan.md`. The document title is **{role['plan_title']}**. Sections: {plan_sections}.
4. Update the diagrams so they match the plan: {diagrams}.
5. Set next action to "wait for plan approval". The reply must be "I approve the plan" or "Skip plan approval".
6. Update the journal.
""",
        ),
    )
    w(
        skills / "diagram-generator" / "SKILL.md",
        skill(
            "diagram-generator",
            "Use when diagrams must be created or rebuilt from the charter and the plan.",
            "Next action is run diagram-generator, or the charter or plan changed",
            f"""# Diagram generator

Rebuild `work-items/<id>/docs/diagrams/` from the charter and the plan.

Diagrams for this role:

{ul(role["diagrams"])}

1. Read `docs/charter/charter.md` and, when it exists, `docs/plan/operating-plan.md`.
2. Write one `.mmd` file per diagram. Use Mermaid flowcharts. Stakeholder and RACI views may be a flowchart or a simple table expressed as a Mermaid block.
3. Write `docs/diagrams/index.html` that lists each diagram and loads Mermaid so the operator can open the file locally.
4. If the next action was "run diagram-generator" inside the planned pipeline, set the next action to "run action-breakdown". If you were only refreshing, leave the next action as it was and note the refresh in the journal.
""",
        ),
    )
    w(
        skills / "action-breakdown" / "SKILL.md",
        skill(
            "action-breakdown",
            "Use when the next action is run action-breakdown. Writes TODOS.md from the approved plan.",
            'Next action is "run action-breakdown"',
            f"""# Action breakdown

1. Read the approved plan. If plan approval is not recorded, stop.
2. Write `TODOS.md` with these sections, in this order:
   - Setup
   - Dependencies and asks
   - Kickoff — include {", ".join(role["kickoff"])}
   - Execution — include concrete actions of these kinds: {", ".join(role["execute"])}
   - Verification — {", ".join(role["verify"])}
   - Communication and close-out
3. Setup and kickoff come before execution.
4. Every execution line has an owner slot and a done check.
5. Set next action to "run kickoff".
6. Update the journal with the task count.
""",
        ),
    )
    w(
        skills / "kickoff" / "SKILL.md",
        skill(
            "kickoff",
            "Use when the next action is run kickoff. Creates the cadence, tracker, decision log, and stakeholder list.",
            'Next action is "run kickoff"',
            f"""# Kickoff

Create the working set from the approved plan before any execute action.

Create these:

{ul(role["kickoff"])}

Suggested paths under the work item:

- `docs/decisions/decision-log.md`
- `docs/trackers/tracker.md` for the tracker named in the kickoff list
- `docs/trackers/cadence.md`
- `docs/trackers/stakeholders.md`

1. If these already exist and match the plan, do not duplicate them. Set the next action to "execute-action (task 1/N)".
2. Otherwise create the missing files from the plan. A decision log starts with columns: date, decision, decider, consequence.
3. If a name or a forum is missing, ask. Do not invent stakeholders.
4. Set next action to "execute-action (task 1/N)" using the count in TODOS.md.
5. Update the journal.
""",
        ),
    )
    w(
        skills / "execute-action" / "SKILL.md",
        skill(
            "execute-action",
            "Use when the next action is execute-action (task K/N). Completes one management action from TODOS.md.",
            'Next action is "execute-action (task K/N)"',
            f"""# Execute action

Complete one item from `TODOS.md`. This is management work. An example output is {role['exec_phrase']}.

Outputs this role produces:

{ul(role["execute"])}

1. Load facts and rules. Follow every rule.
2. {role['never']}
3. Read the TODO. Write the output in the tracker, the decision log, or a note under `docs/notes/`. Mark that TODO done.
4. If you are blocked on a name, a file, or a decision, record the blocker and ask. Do not skip the item.
5. If a people-sensitive note was written, leave it on the work item. Do not copy it to expert-role memory unless the operator says to.
6. If this action changes {role['change_kind']}, stop and start change-request instead of editing the plan in place.
7. Set next action to "execute-action (task K+1/N)", or "run verify" when no items remain.
8. Update the journal.
""",
        ),
    )
    w(
        skills / "verify" / "SKILL.md",
        skill(
            "verify",
            "Use when the next action is run verify. Records acceptance, sign-off, and the risk review.",
            'Next action is "run verify"',
            f"""# Verify

Write `work-items/<id>/docs/verification/verification.md`.

Checks for this role:

{ul(role["verify"])}

1. Compare the checks to the charter and the plan. Cite the success measure.
2. Record stakeholder sign-off as yes, no, or waiting. If waiting, say who.
3. List risks still open.
4. If a check fails, say so and set the next action back to the execute task that must be repeated. Do not close out a failed check unless the operator records an exception.
5. When the checks pass or an exception is recorded, set next action to "run close-out".
""",
        ),
    )
    w(
        skills / "close-out" / "SKILL.md",
        skill(
            "close-out",
            "Use when the next action is run close-out. Writes the status narrative, decision log pointer, and handoff.",
            'Next action is "run close-out"',
            f"""# Close-out

{role['close_out']}

1. Confirm verification exists.
2. Write `docs/close-out/close-out.md` with the status narrative, a link to `docs/decisions/decision-log.md`, and the handoff note (who owns the work next, and what cadence continues).
3. Journal fields to set: status narrative path, decision-log path, handoff note. Do not invent a branch or a review request.
4. Set next action to "done".
5. Ask whether to promote facts and rules.
""",
        ),
    )
    w(
        skills / "change-request" / "SKILL.md",
        skill(
            "change-request",
            "Use when the operator wants to change an approved plan. Covers impact, approval, plan update, execution, and verification.",
            "User asks for a change request, or next action is run change-request",
            f"""# Change request

Use this for {role['change_kind']}.

1. Give the change an id. Create `docs/changes/<change-id>/impact.md` describing what changes, who is affected, and what stays the same.
2. Set next action to "wait for change approval". The phrase is "I approve the change" or "Skip change approval". Continue does not approve.
3. After approval, update `docs/plan/operating-plan.md` and the diagrams. Note the change id in the decision log.
4. Adjust `TODOS.md`. Execute only the actions the change requires, then run verify.
5. Update the journal: mode change-request, current change id.
""",
        ),
    )
    w(
        skills / "improve-ways-of-working" / "SKILL.md",
        skill(
            "improve-ways-of-working",
            "Use when cadence, trackers, or decision logs are duplicated or messy. Cleans them up without changing the agreed outcome.",
            "User asks to improve ways of working, or the next action says so",
            """# Improve ways of working

1. Name the duplication or the mess: two trackers, two cadences, decisions written in more than one place.
2. Propose what will remain and what will be retired. Do not change the approved outcome, scope, or success measure.
3. Wait for the operator to agree.
4. Make the cleanup. Point the journal and STATUS links at the files that remain.
5. Record what changed in the decision log as a hygiene note, not as a new outcome.
""",
        ),
    )
    w(
        skills / "assess-situation" / "SKILL.md",
        skill(
            "assess-situation",
            "Use when the next action is run assess-situation. Opens an escalation assessment.",
            'Next action is "run assess-situation"',
            f"""# Assess situation

Write `docs/escalations/assessment.md`.

This escalation must cover: {role['esc_focus']}

1. Ask what is known and what is still unknown. Unknowns that block the assessment are blocking questions.
2. {role['never']}
3. Set next action to "run analyze-impact".
""",
        ),
    )
    w(
        skills / "analyze-impact" / "SKILL.md",
        skill(
            "analyze-impact",
            "Use when the next action is run analyze-impact. Writes options and waits for response approval.",
            'Next action is "run analyze-impact"',
            f"""# Analyze impact

Write `docs/escalations/impact.md`.

1. State the impact in the terms of this role: {role['esc_focus']}
2. List options and who decides. Include "do nothing yet" when that is honest.
3. Set next action to "wait for response approval". Tell the operator to reply "I approve the response" or "Skip response approval", and to name which option.
4. Do not carry out the response in this step.
""",
        ),
    )
    w(
        skills / "respond" / "SKILL.md",
        skill(
            "respond",
            "Use when the next action is run respond, after response approval.",
            'Next action is "run respond"',
            f"""# Respond

1. Confirm the journal records response approval and which option was chosen. If not, return to the gate.
2. Write `docs/escalations/response.md`: the decision, who was told, the message, and the immediate actions.
3. {role['never']}
4. Carry out only communication and records this expert can write. Do not take over work that belongs to someone else; name that owner in the response.
5. Set next action to "run monitor-situation".
""",
        ),
    )
    w(
        skills / "monitor-situation" / "SKILL.md",
        skill(
            "monitor-situation",
            "Use when the next action is run monitor-situation. Records what is watched and the next check.",
            'Next action is "run monitor-situation"',
            """# Monitor

Write `docs/escalations/monitor.md`.

1. Name the signal, the current reading if known, and the next check time.
2. If the operator does not know the next check time, ask. Do not invent one.
3. Set next action to "run resolve-and-document" when the watch plan is written. Leave the escalation open in the document until that later check is done; say so in the file.
""",
        ),
    )
    w(
        skills / "resolve-and-document" / "SKILL.md",
        skill(
            "resolve-and-document",
            "Use when the next action is run resolve-and-document. Writes the management record of the escalation.",
            'Next action is "run resolve-and-document"',
            """# Resolve and document

Write `docs/escalations/resolution.md`.

Include:

- What was decided
- Who was told, and what they were told
- What remains open, and the next check
- Whether a lasting change should become a change request on the planned pipeline

Set next action to "done". Ask whether to promote any non-sensitive facts or rules.
""",
        ),
    )


def emit_readme():
    w(
        OUT / "README.md",
        """# Manager AI Experts

Each folder is a separate expert. Open the folder as the workspace so its `CLAUDE.md` is the agent contract. The developer expert in `D:\\ClaudeAIExpert` is unchanged.

| Folder | Manager type | Planned workflow | Urgent workflow |
| --- | --- | --- | --- |
| [engineering-manager](engineering-manager) | Engineering manager | Team Delivery | Team Escalation |
| [program-manager](program-manager) | Program manager | Program Delivery | Program Escalation |
| [product-manager](product-manager) | Product manager | Product Initiative | Product Escalation |
| [general-manager](general-manager) | General manager | Management Initiative | Management Escalation |

On the first start, the expert asks you to define the specific role, including notes you already have from doing the job. "Continue" does not answer those questions. After you approve the role, work items use the journal, the charter and plan gates, and the facts and rules for that workflow.
""",
    )


def scan_forbidden():
    hits = []
    for role in ROLES:
        root = OUT / role["folder"]
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            for token in FORBIDDEN:
                if token in text:
                    hits.append(f"{path}: {token}")
    return hits


def main():
    emit_readme()
    for role in ROLES:
        base = OUT / role["folder"]
        if base.exists():
            shutil.rmtree(base)
        emit_claude(role, base)
        emit_myrole(role, base)
        emit_quickstart(role, base)
        emit_workflows(role, base)
        emit_context_and_docs(role, base)
        emit_memory(role, base)
        emit_template(role, base)
        emit_system_skills(role, base)
        emit_domain_skills(role, base)
        copy_support(role, base)
        emit_hooks(role, base)
        subprocess.run(
            [sys.executable, str(base / "scripts" / "memory" / "build_trigger_index.py")],
            check=True,
        )
        print(f"wrote {base}")
    hits = scan_forbidden()
    if hits:
        print("FORBIDDEN HITS:")
        for hit in hits:
            print(hit)
        return 1
    print("forbidden scan clean")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
