#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/../load-env.sh"
uri2hillm 'READ DEVICE sensor-temp REGISTER temperature' \
  | python3 -c "
import json, sys
d = json.load(sys.stdin)
assert d['ok'] is True
assert d['verb'] == 'READ'
assert 'DRY_RUN true' in d['command']
assert d['data']['device_id'] == 'sensor-temp'
"
echo "uri shorthand read ok"
