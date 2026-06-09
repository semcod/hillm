#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/../load-env.sh"
dsl2hillm 'READ DEVICE sensor-temp REGISTER temperature' \
  | python3 -c "
import json, sys
d = json.load(sys.stdin)
assert d['ok'] is True
assert d['data']['device_id'] == 'sensor-temp'
assert d['data']['backend'] == 'dry_run'
assert 'DRY_RUN true' in d['command']
"
echo "dsl read sensor-temp ok"
