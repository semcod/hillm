#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/../load-env.sh"

nlp2hillm 'connect modbus device' --no-llm --apply \
  | python3 -c "
import json, sys
d = json.load(sys.stdin)
assert d['ok'], d.get('error', d)
assert d['command'] == 'CONNECT DEVICE modbus-rtu DRY_RUN true'
assert d['data']['device_id'] == 'modbus-rtu'
"

echo "nlp2hillm connect modbus ok"
