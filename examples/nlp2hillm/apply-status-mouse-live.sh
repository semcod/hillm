#!/usr/bin/env bash
# Live STATUS for mouse — scans /dev/input/by-id (skip when no input subsystem).
set -euo pipefail
source "$(dirname "$0")/../load-env.sh"

if [[ ! -d /dev/input ]]; then
  echo "skip: /dev/input not present" >&2
  exit 0
fi

# load-env sets HILLM_DRY_RUN=1; --live must override for real input scan
unset HILLM_DRY_RUN

nlp2hillm 'what port is the mouse on' --no-llm --apply --live \
  | python3 -c "
import json, sys
d = json.load(sys.stdin)
assert d['ok'], d.get('error', d)
assert d['data']['device_id'] == 'mouse-default'
assert d['data']['backend'] == 'input'
value = d['data'].get('value') or []
assert isinstance(value, list)
mice = [v for v in value if 'mouse' in v.lower()]
assert mice, f'expected mouse entries in {value!r}'
print('mouse entries:', *mice, sep='\n  ')
"

echo "nlp2hillm status mouse live ok"
