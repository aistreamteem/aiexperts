"""Exit 0 if the CSV has the given header names. Usage: csv-has-columns.py <file> col [col ...]"""
import csv
import sys

if len(sys.argv) < 3:
    print("usage: csv-has-columns.py <file.csv> <column> [column ...]", file=sys.stderr)
    sys.exit(1)

path, required = sys.argv[1], sys.argv[2:]
try:
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        header = next(reader, None)
except OSError as e:
    print(e)
    sys.exit(1)

if not header:
    print("empty or no header row")
    sys.exit(1)

have = {c.strip() for c in header}
missing = [c for c in required if c not in have]
if missing:
    print("missing columns: " + ", ".join(missing))
    sys.exit(1)
sys.exit(0)
