# Auto body estimator / office

Collision-shop office Expert: assignment intake, photo indexes, estimate packs from their files, OEM procedure completeness, authorization vs estimate, supplements, parts-vs-estimate, customer-pay split, and cycle time.

- Role: `MyRole.txt`
- How to work: `CLAUDE.md`, `.claude/rules/expert.md`, `docs/role/work-item-method.md`
- Workflows: `.claude/workflows/` (registry: `workflow-registry.json`)
- Memory: `facts/facts-shared.md`, `facts/rules-shared.md`
- Tools: `docs/tools/`
- Work: `work-items/<id>/` with journals under `journals/work-items/<id>/`

Starter facts and rules are **guesses until this shop confirms them**. Hours and prices come only from their labor matrix and parts file. Total-loss stays the insurer’s file.

## Quick start

1. Open **this** folder (the one that contains `MyRole.txt` and `CLAUDE.md`).
2. Read `MyRole.txt` for scope, must-never, and registered jobs.
3. Drop a file you already use (assignment PDF, estimate export, photo folder, portal screenshot).
4. Say which assignment / RO / claim this is so the Expert opens one Work Item under `work-items/<id>/`.
5. Put source files in that Work Item’s `in/` folder (or drop them here and name the claim).
6. Ask for the work. Example: “Here is this week’s assignment and VIN file. Build the intake pack. Do not invent a claim number.”
7. When it finishes, look in **that Work Item’s** `out/` folder.

When it is wrong, tell it (“Hours come from our labor matrix. Do not invent them.”). It should save the correction with **remember**.

## Do not

- Put passwords, bank logins, or card numbers in this folder.
- Ask it to send money or pay a bill.
- Ask it for a total-loss verdict, a structural engineering stamp, or an ADAS calibration stamp.

Each real assignment, RO, or claim gets its own Work Item folder. Do not mix Tuesday’s files into Monday’s pack. Back up the whole folder on a regular schedule.
