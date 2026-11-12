#!/bin/bash
# Stop hook wrapper: merge agent notes + refresh trigger index (Python).
cd "$(dirname "$0")/../.." || exit 0
if command -v py >/dev/null 2>&1; then
  exec py -3 .claude/hooks/on_stop.py
fi
if command -v python3 >/dev/null 2>&1; then
  exec python3 .claude/hooks/on_stop.py
fi
if command -v python >/dev/null 2>&1; then
  exec python .claude/hooks/on_stop.py
fi
printf '{}\n'
exit 0
