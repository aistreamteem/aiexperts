# Checks

Commands a work-map step runs to know if it passed. Exit **0** = pass. Any other exit = fail.

Add scripts here only after the operator approves the command. Do not invent a check for how *this* shop works.

Reusable helpers in this folder:

- `file-exists.py` — every path on the command line must be a file.
- `csv-has-columns.py` — first CSV path; remaining args are required header names.

Run checks against paths inside the active Work Item (`work-items/<id>/work/` and `out/`), not a shared top-level `work/` folder.
