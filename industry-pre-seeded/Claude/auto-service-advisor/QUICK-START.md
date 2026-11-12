# Auto shop service advisor — quick start

This folder is a role role Expert. You do not need to be a programmer.

1. Open **this** folder (the one with `MyRole.txt` and `CLAUDE.md`).
2. Read `MyRole.txt` for the role. Follow `CLAUDE.md` and `.claude/rules/expert.md`.
3. Method: `docs/role/work-item-method.md`. Typical ticket starts with the **One RO** job.
4. Shop facts/rules live under `facts/` (shared + operations memory). Work maps live under `.claude/workflows/` (listed in `workflow-registry.json`). Tools live under `docs/tools/`.

## First real job

1. Save a file you already use (RO PDF/export, MPI form, parts confirmation, invoice).
2. Tell the chat which ticket this is (for example RO 5521). It should use `work-items/<id>/` so this RO does not mix with the last one.
3. Put the file in that Work Item’s `in/` directory, or drop it here and say which RO it belongs to.
4. Ask for the work. Example: “Here is today’s RO export. Make the write-up pack. Do not invent a cause.”
5. When it finishes, look in **that Work Item’s** `out/` folder.

## When it is wrong

Tell it in shop words: “We call that a ticket, not a work order.” “Never put card numbers on the pack.” “Book time comes from our Mitchell sheet.” It should **remember** the correction.

The notes already here are a **head start** — typical US counter practice, not how *your* shop works until you say so.

## Do not

- Put passwords, bank logins, or card numbers in this folder.
- Ask it to send money or pay a bill.
- Ask it to certify inspections, give emissions legal advice, or invent a diagnosis.

Copy the **whole folder** somewhere safe on a regular schedule. The starter is not a backup of *your* Expert.
