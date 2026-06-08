#!/usr/bin/env bash
# Live serial read — skip when pyserial or serial port missing.
set -euo pipefail
source "$(dirname "$0")/../load-env.sh"

if ! python3 -c "import serial" 2>/dev/null; then
  echo "skip: pyserial not installed (uv sync --extra serial)" >&2
  exit 0
fi

port="${HILLM_SENSOR_TEMP_ADDRESS:-/dev/ttyACM0}"
if [[ ! -e "$port" ]] && [[ ! -e /dev/ttyUSB0 ]]; then
  echo "skip: no serial port ($port or /dev/ttyUSB0)" >&2
  exit 0
fi

export HILLM_SENSOR_TEMP_ADDRESS="${HILLM_SENSOR_TEMP_ADDRESS:-$port}"
unset HILLM_DRY_RUN

nlp2hillm 'read temperature from serial' --no-llm --apply --live \
  | python3 -c "
import json, sys
d = json.load(sys.stdin)
assert d['ok'], d.get('error', d)
assert d['data']['device_id'] == 'sensor-temp'
assert d['data']['backend'] == 'serial'
print('serial read value:', repr(d['data'].get('value')))
"

echo "nlp2hillm temperature live ok"
