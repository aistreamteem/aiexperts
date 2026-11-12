#!/bin/bash
# Thin PreToolUse wrapper. Logic lives in inject_journal_context.py.
cd "$(dirname "$0")/../.." || exit 0
if command -v py >/dev/null 2>&1; then
  exec py -3 .claude/hooks/inject_journal_context.py
fi
if command -v python3 >/dev/null 2>&1; then
  exec python3 .claude/hooks/inject_journal_context.py
fi
if command -v python >/dev/null 2>&1; then
  exec python .claude/hooks/inject_journal_context.py
fi
exit 0
