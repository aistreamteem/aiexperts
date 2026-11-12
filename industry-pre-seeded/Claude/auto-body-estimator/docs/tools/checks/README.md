# Checks

Commands a workflow step runs to know if it passed. Exit **0** = pass. Any other exit = fail.

Add a helper here only after the operator approves how *this* shop proves the step. Do not invent a check for how *this* business works.

Reusable helpers in this folder:

- `file-exists.py` — every path on the command line must be a file.
- `csv-has-columns.py` — first CSV path; remaining args are required header names.

Run checks against paths **inside the current Work Item folder** (`work-items/<id>/`).
