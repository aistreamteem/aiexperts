# Checks

Commands a workflow step runs to know if it passed. Exit **0** = pass. Any other exit = fail.

Do not invent a check for how *this* shop works. If a step has no check, ask the operator how they will know it is done, then save the approved command here.

Reusable helpers in this folder:

- `file-exists.py` — every path on the command line must be a file.
- `csv-has-columns.py` — first CSV path; remaining args are required header names.

Run checks against paths **inside the current Work Item** (`work-items/<id>/work/` and `out/`).
