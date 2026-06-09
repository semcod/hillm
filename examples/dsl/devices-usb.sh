#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/../load-env.sh"
dsl2hillm 'DEVICES CATEGORY usb' \
  | python3 -c "
import json, sys
d = json.load(sys.stdin)
assert d['ok'] is True
assert d['verb'] == 'DEVICES'
"
echo "dsl devices usb ok"
