#!/bin/bash
# SubagentStop uses the same Python entry point as Stop.
exec "$(dirname "$0")/on-stop.sh"
