# Checks

Commands a work-map step runs to know if it passed. Exit **0** = pass. Any other exit = fail.

If a step has no check, propose one and get the operator's approval before saving a script here. Do not invent a check for how *this* shop works.

Reusable helpers in this folder:

- `file-exists.py` — every path on the command line must be a file.
- `csv-has-columns.py` — first CSV path; remaining args are required header names.
