# Checks

Commands a work-map step runs to know if it passed. Exit **0** = pass. Any other exit = fail.

Do not invent a check for how *this* center works. If a step has no check, ask with **operator-qa**.

Reusable helpers in this folder:

- `file-exists.py` — every path on the command line must be a file.
- `csv-has-columns.py` — first CSV path; remaining args are required header names.
