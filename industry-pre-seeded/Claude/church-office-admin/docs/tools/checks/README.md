# Checks

Commands a workflow step runs to know if it passed. Exit **0** = pass. Any other exit = fail.

Add a new script here only after the operator approves it. Do not invent a check for how *this* office works.

Reusable helpers in this folder:

- `file-exists.py` — every path on the command line must be a file.
- `csv-has-columns.py` — first CSV path; remaining args are required header names.

Run these against paths inside the current Work Item (`work-items/<id>/work/…` or `out/…`).
