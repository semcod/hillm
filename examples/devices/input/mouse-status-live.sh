#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/../../load-env.sh"

if [[ ! -d /dev/input ]]; then
  echo "skip: /dev/input not present" >&2
  exit 0
fi

unset HILLM_DRY_RUN
hillm status --device mouse-default \
  | python3 -c "
import json, sys
d = json.load(sys.stdin)
assert d['ok'] is True
assert d['backend'] == 'input'
value = d.get('value') or []
mice = [v for v in value if 'mouse' in v.lower()]
assert mice, f'expected mouse entries, got {value!r}'
"

echo "input mouse status live ok"
