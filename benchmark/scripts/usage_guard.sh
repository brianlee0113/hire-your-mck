#!/bin/bash
# Print the 7-day utilization (0-1) of the logged-in Claude account; exit 1 if it is at or above $1 (default 0.80).
lim=${1:-0.80}
u=$(echo "Reply with OK." | claude -p --model claude-haiku-5-5 --output-format stream-json --verbose --setting-sources "" --strict-mcp-config 2>/dev/null \
  | grep -o '"seven_day":{"utilization":[0-9.]*' | head -1 | grep -o '[0-9.]*$')
echo "seven_day utilization: ${u:-unknown}"
[ -z "$u" ] && exit 0
python3 -c "import sys; sys.exit(1 if float('$u') >= float('$lim') else 0)"
