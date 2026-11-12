"""Exit 0 if every argument is an existing file. Else print missing paths and exit 1."""
import os
import sys

if len(sys.argv) < 2:
    print("usage: file-exists.py <path> [path ...]", file=sys.stderr)
    sys.exit(1)

missing = [p for p in sys.argv[1:] if not os.path.isfile(p)]
if missing:
    for p in missing:
        print(f"missing: {p}")
    sys.exit(1)
sys.exit(0)
