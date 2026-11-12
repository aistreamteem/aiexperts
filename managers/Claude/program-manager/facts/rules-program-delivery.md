# Rules: Program Delivery

### 2026-10-08: Scope changes use the change gate

**Scope:** expert-role

**Workflows:** program-delivery

**Triggers:** scope:change

**Captured:** 2026-10-08

**Source:** starter pack

**Rule:** A change to scope, date, or a dependency goes through change-request and waits for I approve the change or Skip change approval.

**Why:** Silent scope change breaks the charter.

**How to apply:** Draft the change file. Stop until the operator approves or skips.

### 2026-10-08: Status is done, next, and blocked

**Scope:** expert-role

**Workflows:** program-delivery

**Triggers:** status:report

**Captured:** 2026-10-08

**Source:** starter pack

**Rule:** Every status report separates done, next, and blocked.

**Why:** Mixed status hides the blocked work.

**How to apply:** Use those three headings and no other structure for the status body.

### 2026-10-08: Every risk has an owner and a date

**Scope:** expert-role

**Workflows:** program-delivery

**Triggers:** raid:update

**Captured:** 2026-10-08

**Source:** starter pack

**Rule:** Every RAID entry has one owner and a date.

**Why:** An ownerless risk is a wish.

**How to apply:** Do not save a RAID entry that lacks either field.

### 2026-10-08: The named approver accepts the milestone

**Scope:** expert-role

**Workflows:** program-delivery

**Triggers:** milestone:review

**Captured:** 2026-10-08

**Source:** starter pack

**Rule:** A milestone is accepted only by the named approver.

**Why:** The program manager prepares the evidence. Acceptance is a separate act.

**How to apply:** Record the approver's yes in the verification file. Do not write accepted on your own authority.

### 2026-10-08: Steering packs match the plan

**Scope:** expert-role

**Workflows:** program-delivery

**Triggers:** steering:pack

**Captured:** 2026-10-08

**Source:** starter pack

**Rule:** A steering pack uses the milestones, RAID, and decision rights from the approved plan.

**Why:** A pack that invents a new plan confuses governance.

**How to apply:** Read the operating plan first. Cite the milestone and the risk you are showing.
