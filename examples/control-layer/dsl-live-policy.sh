#!/usr/bin/env bash
# dsl2hillm hardware verbs default to dry-run; --live skips DRY_RUN.
set -euo pipefail
source "$(dirname "$0")/../load-env.sh"

dsl2hillm 'READ DEVICE sensor-temp' \
  | python3 -c "
import json, sys
d = json.load(sys.stdin)
assert d['ok'] is True
assert 'DRY_RUN true' in d['command']
"

unset HILLM_DRY_RUN
if ! python3 -c "import serial" 2>/dev/null; then
  echo "skip: pyserial not installed for --live check" >&2
  exit 0
fi
dsl2hillm 'READ DEVICE sensor-temp' --live \
  | python3 -c "
import json, sys
d = json.load(sys.stdin)
assert 'DRY_RUN' not in d['command']
"

echo "dsl live policy ok"
