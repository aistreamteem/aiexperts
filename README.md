# AI Experts

AI Experts are **virtual employees**. Each expert learns a real job role from the people who already do that work, then helps them and their team get more done—first as a capable assistant, then by taking on more of the routine work over time.

## How it works

1. **Learn the role from existing employees**  
   An expert starts by capturing how the job is actually done: responsibilities, workflows, tools, judgment calls, and team norms. Notes, docs, and answers from the people in the role become the expert’s baseline.

2. **Build durable memory**  
   Facts, rules, and journals store what the expert knows and what it has done. That memory carries across sessions so the expert does not start from zero every time.

3. **Assist day to day**  
   The expert works alongside the employee and their team—drafting plans and charters, breaking down work, tracking status, producing artifacts, answering questions, and keeping context organized.

4. **Automate more over time**  
   As the role definition and memory mature, repeatable work moves from “help me with this” to reliable, guided execution. Humans stay in control of decisions; the expert takes on more of the execution and continuity.

The goal is not to replace the team. It is to give every role a virtual teammate that learns their craft, reduces busywork, and scales their expertise.

## What’s in this repo

Experts are packaged as folders you open as a workspace in **Claude** or **Cursor**. Each folder includes role definitions, skills/workflows, memory, and journals.

| Path | What you get |
| --- | --- |
| [`developers/`](developers/) | Software developer experts (Claude and Cursor) that turn specs into design, tasks, code, and tests. |
| [`managers/`](managers/) | Manager experts—engineering, product, program, and general manager—for delivery, initiatives, and escalations. |
| [`industry-pre-seeded/`](industry-pre-seeded/) | Role experts pre-seeded for common industry jobs (leasing, clinics, bookkeeping, dispatch, and many others), ready to customize for a specific shop. |

Each category has Claude and Cursor variants so you can run the same kind of virtual employee in the environment your team already uses.

## Getting started

1. Pick a role folder that matches the job (or start from a close industry seed).
2. Open that folder as the workspace in Claude or Cursor.
3. Follow the folder’s `QUICK-START.md` (or `README.md`) and define the role with input from the real employee.
4. Run work through **Work Items** so progress, decisions, and learnings stay in the journal and memory.
5. Promote useful facts and rules as the expert learns how *your* team works.

Over successive work items, the expert becomes a stronger assistant for that employee and a shared source of continuity for their team.
