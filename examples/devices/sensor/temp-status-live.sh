#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/../../load-env.sh"

port="$(python3 -c "
from hillm.registry import get_device_spec
print(get_device_spec('sensor-temp').resolve_address())
")"

if [[ ! -e "$port" ]]; then
  echo "skip: serial port missing ($port)" >&2
  exit 0
fi

unset HILLM_DRY_RUN
hillm status --device sensor-temp \
  | python3 -c "
import json, sys
d = json.load(sys.stdin)
assert d['ok'] is True
assert d['backend'] == 'serial'
assert d['data']['exists'] is True
"

echo "sensor temp status live ok ($port)"
