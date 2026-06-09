#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/../load-env.sh"
hillm status --device mouse-default --dry-run \
  | python3 -c "
import json, sys
d = json.load(sys.stdin)
assert d['ok'] is True
assert d['device_id'] == 'mouse-default'
"
echo "status mouse dry-run ok"
