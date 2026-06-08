#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/../load-env.sh"

nlp2hillm 'read temperature from serial' --no-llm --apply \
  | python3 -c "
import json, sys
d = json.load(sys.stdin)
assert d['ok'], d.get('error', d)
assert d['command'] == 'READ DEVICE sensor-temp REGISTER temperature DRY_RUN true'
assert d['data']['device_id'] == 'sensor-temp'
assert d['data']['backend'] == 'dry_run'
"

nlp2hillm 'read usb port for mouse' --no-llm --apply \
  | python3 -c "
import json, sys
d = json.load(sys.stdin)
assert d['ok'], d.get('error', d)
assert d['data']['device_id'] == 'mouse-default'
"

echo "nlp2hillm apply dry-run ok"
