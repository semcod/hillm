#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/../load-env.sh"
hillm status --ecosystem \
  | python3 -c "
import json, sys
d = json.load(sys.stdin)
assert d['ok'] is True
assert d['devices_registered'] >= 10
"
echo "status ecosystem ok"
