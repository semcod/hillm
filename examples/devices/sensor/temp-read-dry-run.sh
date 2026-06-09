#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/../../load-env.sh"
hillm read --device sensor-temp --register temperature --dry-run \
  | python3 -c "
import json, sys
d = json.load(sys.stdin)
assert d['ok'] is True
assert d['device_id'] == 'sensor-temp'
assert d['backend'] == 'dry_run'
assert d['value'] == 'dry:temperature'
"
echo "sensor temp read dry-run ok"
