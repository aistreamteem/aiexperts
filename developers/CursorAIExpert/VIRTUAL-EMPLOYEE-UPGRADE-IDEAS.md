# Upgrade ideas: from expert scaffold to independent virtual employee

Written 2026-11-09 from a read-through of this folder and a few probes of the hook scripts. I read `AGENTS.md`, the hooks, the workflow and memory docs, the templates, and 10 of the 17 skills in full (continue, define-role, remember, journal-keeper, memory-optimize, integrate-docs, promote-facts-rules, operator-qa, implement-feature, workflow-selector); the other seven I only searched. Nothing in the scaffold was changed. File and field names proposed below are suggestions, not existing things, unless a path is given.

## Summary

Today the scaffold is an operator-driven assistant. A person opens Cursor and types "continue"; the agent performs one pipeline step, records it, and stops for approval. What it already does well is worth keeping: resumable journals, work-item isolation, two-level memory with promotion, rules surfaced at the moment of an action, and strict handling of approvals ("continue" is never an answer).

Five things separate that from an employee who can be left alone with the job:

1. **It only acts when spoken to.** There is no inbox, backlog, schedule, or way to run without a person at the keyboard.
2. **Its rules are advice.** The hooks inject rule text. Nothing blocks a forbidden action or checks that a rule was followed.
3. **The human is the only quality control.** Nothing verifies work before it is handed over, and nothing measures whether the expert is competent at the role.
4. **Its knowledge model is narrower than a person's.** Facts and rules have a home. Tools, people, past cases, judgement, and "how stale is this" do not.
5. **It is hard-wired to one job:** a software developer running an HLD/DD pipeline.

Separately, the scaffold has internal breakage (section 3): missing skills, three generations of journal paths, hooks that misread their own templates. That should be repaired first, because several mechanisms the ideas build on do not currently work as written.

If only three things get built, I would pick the cross-work-item decision queue with a real backlog (2.1, 2.8), enforced guardrails with saved evidence (2.3), and a scenario suite that tests the expert itself (2.9). Those are what let the human stop watching.

## 1. The gap at a glance

| A person in the role | The scaffold today | Gap |
| --- | --- | --- |
| Picks up work from tickets, mail, chat, calendar | Work starts only from a chat message | Intake, backlog, scheduled wake-up |
| Juggles several tasks; switches when blocked | One global active work item; stops when blocked | Waiting states, wake conditions, next-item selection |
| Knows what they may decide alone | Fixed gates per pipeline; asks on every blocker | Decision rights by action class; autonomy earned over time |
| Cannot do what policy forbids (access controls, reviews) | Rule text injected as context; hooks always allow | Blocking guardrails; evidence requirements |
| Knows their tools and has accounts | No tool registry, credentials model, or identity | Tool catalogue, access checks, own account |
| Knows people, history, examples, quality bars | Facts and rules only | More kinds of knowledge; freshness; retrieval at scale |
| Reviews own work before handing over | Human gate is the only check | Self-review, acceptance criteria, evidence |
| Learns from feedback and mistakes | "Remember this" one entry at a time, human-approved | Retrospectives, batch review, learning from outside feedback |
| Reports status, escalates, writes to stakeholders | Chat with one operator; per-item `STATUS.md` | Decision queue, digest, outbound communication policy |
| Was interviewed, onboarded, and is appraised | Two hook tests | Scenario suite, shadow period, operating metrics |
| Could be an analyst, an SRE, a support engineer | "You are the project builder" | Role-neutral kernel plus role packs |

## 2. Ideas

### 2.1 Work arrives and gets picked up without a prompt

**Today:** all work begins with a chat message. One global pointer (`.cursor/active-context.txt`) names the single active work item. "Future work" in `journals/expert/progress.md` is a free-text list. The work-item journal has no requester, priority, due date, or acceptance criteria.

- **Intake channels.** Connect the places work comes from for the role (issue tracker, chat mentions, email, alerts, review requests) through MCP servers. Add a triage skill that turns each incoming item into a backlog record: who asked, what for, how urgent, which workflow, and whether it is inside the role's remit at all.
- **A real backlog.** Replace the free-text "Future work" with a structured queue, one record per item: requester, priority, due date, acceptance criteria, state, who or what it is waiting on, and the condition that wakes it.
- **Several work items in flight.** A person blocked on a review picks up something else. Make "waiting" a first-class state with a wake condition (approval arrived, CI finished, a date reached), and have the agent select the next runnable item instead of stopping.
- **A heartbeat.** A scheduled run (Cursor Automations, the CLI, or the SDK) that wakes the agent to check intake, check wake conditions, advance whatever is runnable, and write the digest.
- **Recurring duties.** A list in the role definition of things done on a calendar (weekly report, dependency review, on-call checks), each mapped to a workflow. The heartbeat opens the work item when one falls due.
- **A lane for small work.** Much of a job is questions, reviews, and ten-minute fixes. Requiring a WID and a pipeline choice for each is too heavy. Add a lightweight work type that costs one journal line.

### 2.2 Delegated authority instead of fixed gates

**Today:** gates are fixed per pipeline (HLD, DD, feature design). `AGENTS.md` rules 7 and 16 tell the agent to stop and ask on any blocker. define-role question 3 collects the role's decision rights, and nothing downstream reads the answer.

- **A decision-rights table.** Machine-readable, per action class, with four levels: act; act and report; propose and wait; never. Define the classes by reversibility and blast radius (edit in a branch, push to main, change production, send an external message). Skills and hooks both read it.
- **Approvals that do not block the queue.** A gate becomes a request written to the decision queue (2.8). The agent parks that item and moves to the next one. Record who approved, when, and through which channel.
- **Earned autonomy.** Track outcomes per gate. After a set number of consecutive approvals with no changes requested, propose to the human that the gate drop to "act and report". A rejection or an incident resets it. Autonomy then grows on evidence instead of by a switch.
- **Assume and disclose for low-stakes unknowns.** For reversible, low-impact questions, let the agent choose, record the assumption where the reviewer will see it, and continue. Keep blocking for the high-impact class.
- **Budgets.** Time, cost, and retry limits per work item. Exceeding one is itself an escalation.

### 2.3 Rules that are enforced, not just shown

**Today:** both `preToolUse` hooks always return `continue: true`; they can add context and nothing else. The trigger classifier in `.cursor/hooks/inject_rules_on_action.py` is hard-coded Python for an earlier role's vocabulary (`.sql` files, HTML under outputs/, `gh pr create`). I ran it: an MCP tool call and `kubectl apply -f prod.yaml` match nothing, while `git config user.name x` matches `config:change`.

- **Blocking guardrails.** Turn the "never do" list (define-role question 7) and the "never" level of the decision-rights table into hook rules that deny the call or require confirmation. Cursor's hook contract has allow, deny, and ask responses for shell and MCP calls as far as I know; confirm against the current hooks documentation before designing around it.
- **Triggers as data.** Move trigger definitions out of the classifier into a file each role owns: token, tool names, path globs, command patterns, MCP tool names. A finance or support role can then define `send:outbound-email` or `ledger:post` without editing Python.
- **Triggers for facts.** Facts are browse-only today. Let a fact attach to an entity (a repository, a system, an account, a path) so it surfaces when the agent touches that entity.
- **Evidence requirements.** "Tests pass" is currently a sentence the agent writes in the journal. Require an artefact: the command and its output saved under the work item. A hook on `git push` or on stop refuses when the evidence is missing or older than the last edit.
- **A compliance log.** Have the hook append every injection and every denial to an append-only log. That shows which rules fire, which never do, and which were shown and then ignored.

### 2.4 Tools and access as part of the role

**Today:** tools are part of the stated concept, but the folder has no tool registry, no MCP configuration, and no notion of credentials or of the agent's own identity.

- **A tool catalogue.** Per system: what it is for, how it is reached (MCP, CLI, API, browser), read or write, risk class, the name of the credential (never the secret), usage notes, and the date it was last verified working.
- **An access-check skill.** Smoke-test each tool and record the result. Run it at onboarding and on the heartbeat, so broken access is found before a task needs it.
- **An access onboarding checklist.** The equivalent of a new hire's first-week provisioning: accounts, repositories, permissions, each with a status.
- **Its own identity.** A named account for commits, comments, and messages, so its actions are attributable and revocable, with a standard line disclosing that the author is an AI.
- **A secrets policy.** Memory files are committed and pushed to GitHub. Add a pre-commit scan and a rule that credentials are referenced by name, not stored.

### 2.5 A fuller knowledge model

**Today:** two kinds of entry (fact, rule), two scopes (work item, expert role), filed by workflow and loaded as whole files. Metadata is capture date, source, and status.

**Kinds of knowledge with no home**

- **People and ownership:** who requests work, who approves what, who owns which system, preferred channel, escalation path.
- **Past cases:** completed work items are not indexed. Add a closing summary card (problem, approach, outcome, lessons) and search those cards at intake for similar earlier work.
- **Worked examples:** approved deliverables kept as exemplars per type, and rejected ones with the reason. Judgement is passed on mostly by example.
- **Quality bars:** a definition of done per deliverable type, not one global definition.
- **Glossary and system map:** the vocabulary and the landscape a new hire absorbs in the first month.
- **Priorities:** what wins when two rules conflict, such as speed against thoroughness during an incident.

**Trust and freshness**

- Add to each entry: confidence, last-verified date, review-by date, supersedes and superseded-by links, and for checkable facts a command that verifies them. When the agent is about to rely on a fact past its review date, it verifies it or flags it.
- State one precedence order for conflicts (for example: work item over role, newer over older, human-stated over inferred).

**Retrieval that scales**

- The memory docs describe whole-file loading at about 1,300 lines per workflow, and that was already a problem that needed an optimisation pass. A fully populated role will have thousands of entries. Move to one entry per card with tags (topic, entity, trigger), a generated index, and search on demand. Ripgrep over tags is enough to start; a full-text or embedding index can come later. Load a small always-on core plus whatever the task retrieves.

**Getting knowledge out of the human**

- define-role asks 11 questions and ingests documents, but most expertise is not written down. Add elicitation skills: a structured interview per responsibility area; "walk me through the last time you did this"; a shadow mode where the human does a task while the agent records the steps and asks why; and scenario questions ("what would you do if...") whose answers become rules.
- **A coverage map:** responsibilities from the role definition against the count and freshness of knowledge for each, so thin areas are visible.
- **A gap log:** every question the agent had to ask gets logged with its topic. Repeats are the best signal of what to capture next.

### 2.6 Checking its own work

**Today:** quality control is the human gate. `.cursor/workflows/developer.md` even hands test execution to the user ("Inform user to run full build and test suite", then wait for confirmation), which contradicts `AGENTS.md` rules 11 and 14.

- **Acceptance criteria** written at intake and checked at close.
- **An independent review pass.** A subagent with fresh context receives only the request, the acceptance criteria, the applicable rules, and the deliverable, and is asked to find faults. Findings are fixed or recorded before the human sees the work.
- **Per-deliverable checklists** drawn from the quality bars in 2.5.
- **The agent runs the tests** and saves the output as evidence (ties to 2.3).
- **Stuck detection.** The same failure three times, or a budget exceeded, means stop, summarise, and escalate.
- **A handoff statement:** what was verified, what was not, and where the reviewer should look.

### 2.7 Learning from experience

**Today:** learning is one entry at a time, each with a classification dialogue of up to four questions (the remember skill), plus promotion at the end of a work item. Only pipelines can be proposed as new procedure.

- **A retrospective at close.** What was reworked, what had to be asked, what the gate comments said, and which rule would have prevented it. The output is a set of candidate entries.
- **A candidate inbox.** Proposals queue in one place and are reviewed in a batch instead of interrupting work with four questions each. The agent pre-fills type, scope, workflow, and trigger; the human accepts, edits, or rejects.
- **Learning from outside feedback:** review comments, CI failures, reopened tickets, stakeholder replies.
- **Skill authoring.** When the same multi-step procedure is done a third time, propose a new skill. Skills are the procedural memory, and no path currently grows them.
- **Retirement.** Use the compliance log to find rules that never fire and facts never retrieved, and propose archiving them. memory-optimize handles only size and duplicates.
- **Self-knowledge.** A record of where the agent has failed (task types, tools), consulted when planning and when deciding whether to ask for review.

### 2.8 Communication

**Today:** one operator, in chat, with a `STATUS.md` per work item. `NEEDS-ATTENTION.md` exists only for failed background tasks.

- **One decision queue at the root.** Every approval, blocking question, candidate memory entry, and escalation across all work items, in one file or view, each with the agent's recommendation. The human's daily cost becomes reading one page.
- **A daily digest:** done, in progress, waiting on whom, decisions needed, risks.
- **Outbound messages.** A skill and a policy for writing to people other than the operator (ticket comments, PR descriptions, chat, email): who may be contacted, through what, in what tone, and which messages need approval first. Start with drafts only.
- **Asking the right person.** With the people map from 2.5, route a question to the owner instead of always to the operator.
- **An overview:** all work items and their states on one page, as a Canvas or with the existing visual-page skill.

### 2.9 Proving competence

**Today:** two hook tests in `scripts/`, which pass. Nothing tests skill behaviour or performance in the role, and nothing shows whether a change to a rule or skill made the expert worse.

- **A scenario suite per role.** Real past tasks with known good outcomes, run headless and scored against checks ("asked about X before designing", "did not push without tests", "applied rule Y"). Run it after every change to `AGENTS.md`, a skill, or the core rules. It is the regression test for the expert itself.
- **An onboarding exam.** The bar for each autonomy level is passing a set of scenarios, the way a new hire is supervised until they have shown they can do the work.
- **A shadow period.** For a few weeks the agent works incoming tasks in parallel with the human without acting, and the results are compared.
- **Operating metrics:** approved-without-change rate, rework rate, questions per work item, repeat-question rate, guardrail denials, cycle time, cost per item. These feed both earned autonomy (2.2) and the learning loop (2.7).
- **CI for the scaffold:** run the hook tests and an integrity check (section 3) on every commit.

### 2.10 One kernel, many roles

**Today:** `AGENTS.md` opens with "You are the project builder". define-role says "The folder stays a software developer expert". About ten of the 24 rules concern HLD, DD, tests, or git.

- **Split the kernel from the role.** The kernel is role-neutral: state, journals, memory, authority, intake, learning, communication. A role pack holds workflows, phase skills, triggers, the tool catalogue, templates, quality bars, and the scenario suite. Developer becomes the first pack.
- **Role packs as folders** that can be copied, versioned, and shared between people in the same job.
- **Workflows as data.** Phases, entry and exit criteria, gate class, artefacts, and the skill for each phase, in a file the kernel reads. Today `continue/SKILL.md` hard-codes the phase list, so adding a workflow means editing continue, journal-keeper, and spec-parser.
- **Work that is not a pipeline:** an investigation, a review, an advisory answer, a recurring report.
- **A deeper role definition:** service levels, working hours, stakeholders, what good looks like, known hard cases.

### 2.11 Running unattended, safely

**Today:** it runs inside an open IDE with a person present. One global pointer selects the active context. State lives in markdown read by line-prefix matching. The stop hooks need `bash` and `jq`.

- **A headless runtime** for the heartbeat in 2.1, with the same hooks and guardrails as the interactive one.
- **Structured state.** Keep machine-read fields (workflow type, phase, next action, status, approvals) in JSON and generate the markdown for people. `state.json` already does this for the branch map.
- **Per-session context.** Replace the global pointer so two sessions or agents cannot redirect each other.
- **All hooks in Python,** with no `bash` or `jq` dependency. The two journal hooks already are.
- **Untrusted input.** Once tickets, emails, and web pages flow in, they become a route for instructions the operator never gave. Treat external content as data, never let it write to memory or change rules without human review, and keep its provenance on every entry derived from it. This has to land before intake channels go live.
- **An action log.** An append-only record of every action with an outside effect, with the work item, the authority level, and the approval that covered it.
- **Checkpoint and rollback.** The spec doc lists this as out of scope for v1. Unattended operation needs it: a branch or tag before large steps, and a documented undo for each "act and report" action class.
- **A pause switch.** One file or command that stops all unattended activity.

## 3. Defects to fix first

The fix for each item, with later corrections to this table, is in `EXPERT-REPAIR-PLAN.md`.

"Ran" means I executed something to confirm it. "Read" means I found it by reading the files and did not exercise it.

| # | Finding | Basis | Effect |
| --- | --- | --- | --- |
| 1 | Four phase "skills" do not exist: hld-writer, dd-writer, task-breakdown, git-workflow. `AGENTS.md` rule 17, define-role question 6, and the continue skill refer to them as skills; the README says they are phases without folders. Their entire definition is three to six bullets each in `.cursor/workflows/developer.md`. implement-feature also defers to a test-writer that does not exist, and `docs/design/hld-profiles.md` and `hld-extended-sections.md` (rule 8) are missing. | Ran (path checks) | The design phases, which are the core of the developer pipeline, run on almost no instruction. |
| 2 | None of the six expert memory files (`facts/facts-*.md`, `facts/rules-*.md`) exists, and there is no template for them. The documented entry formats disagree: `##` headers in remember and promote-facts-rules, `###` in `MEMORY-INDEX.md` and integrate-docs. The integrate-docs rule format has no `Triggers:` field. The memory-optimize metrics regex (`^###\d{4}`) has no space after the hashes. | Ran (path checks); read | The first capture creates files ad hoc. Bulk-imported rules never reach the action hook. The health check would count zero entries. |
| 3 | Three generations of journal location coexist. The current one is `journals/work-items/<id>/`. implement-feature still names `work-items/<id>/journal/progress.md` as the journal. `post-journal-update.sh` commits that pointer file, not `journals/`. `merge-agent-notes.sh` looks for notes under `work-items/*/journal/agent-notes`. Fifteen files reference the legacy `active-work-item.txt`, and `post-journal-update.sh` reads only that one. | Read | The audit trail snapshots the wrong file, and skills disagree on where to write. |
| 4 | The journal hook cannot read bolded fields. The templates write `**Current work item:**` and `**Completion status:**`; the hook matches lines that start with the unbolded text. | Ran | The fallback work-item lookup returns nothing and "done" is never detected. The tests pass only because their fixtures use unbolded lines. |
| 5 | Trigger classifier faults: `git config` fires `config:change`; path-scoped deliverable tokens disagreed with the vocabulary; `write:doc` is emitted and was not listed; a `.sql` file under `/outputs/` was mis-tagged. | Ran | Wrong rules are shown, and some tagged rules can never be shown. |
| 6 | On this machine `bash` resolves to WSL (`C:\WINDOWS\system32\bash.exe`), which has no `jq`. Git Bash, which the README requires, is not at its default path. `merge-agent-notes.sh` returns early for every session when `jq` is absent; the Python fallback below that check is unreachable. | Ran (environment); read (script logic) | The background-agent note merge never happens here, and the stop hooks depend on WSL being present. |
| 7 | Leftovers from an earlier, populated role. The memory docs cite line counts and files that do not exist. The production-incident workflow is described in continue, journal-keeper, workflow-selector, and `workflows/README.md`, but it is not in the registry and has no workflow file. Domain terms remain (DBHS, CCE, SRM Studio, an NUnit path). The remember skill says memory was split "since 2027-01-01", which is in the future. A search-and-replace turned "w-" into "WID-": `workflowID-registry.json`, "folloWID-up", `newID-workflow`. | Read | The agent is told about files and workflows that are not there, and `workflows/README.md` gives the wrong filename for the registry. |
| 8 | Backslash-escaped markdown (`\#`, `\*\*`) in `HOW-MEMORY-LOADING-WORKS.md`, `MEMORY-INDEX.md`, the spec doc, and the work-item `facts/` templates. | Read | Headings do not render, and a new work item's facts files start with syntax the entry parsers will not match. |
| 9 | `AGENTS.md` contradicts the skills. Rule 19 puts all state in `work-items/<id>/` while rule 2 says `journals/`. Rules 15 and 21 name `facts/facts.md` and `facts/rules.md`, which the skills say are archived. | Read | The one file loaded on every turn is the least current. |

One addition would have caught most of this table: an integrity-check script that confirms every path and skill name referenced in `AGENTS.md`, the skills, and the hooks exists, that the trigger vocabulary agrees across files, and that the templates parse. Run it in CI with the hook tests.

## 4. Suggested order

Each stage is useful on its own and is the precondition for trusting the next.

| Stage | Goal | Contents |
| --- | --- | --- |
| 0 | The scaffold does what it says | Section 3 repairs, integrity check, hooks in Python, structured state (2.11) |
| 1 | Trustworthy when supervised | Blocking guardrails, triggers as data, evidence (2.3); self-review (2.6); knowledge metadata and card-based retrieval (2.5); candidate inbox and retrospective (2.7) |
| 2 | Works a queue with light supervision | Backlog and waiting states (2.1); decision rights (2.2); decision queue and digest (2.8); tool catalogue (2.4); kernel and role-pack split (2.10) |
| 3 | Unattended | Untrusted-input handling, action log, pause switch (2.11), then heartbeat and intake channels (2.1); scenario suite and shadow period (2.9); earned autonomy (2.2) |

## 5. Decisions that shape the design

These are yours to make, and the answers change what gets built first.

1. **Which role gets populated first, and is it a developer role?** If not, the kernel and role-pack split (2.10) moves to stage 0.
2. **Where will it run unattended:** this workstation, Cursor's cloud agents, or a CI runner? That decides how hooks, credentials, and tool access work.
3. **Which channels may it read, and which may it write to?** Reading tickets is low risk. Sending email as the role is not.
4. **What is the first thing it may do without asking?** Naming one concrete action class makes the decision-rights table real.
5. **One operator or several approvers?** With several, approvals need identity and routing from the start.
