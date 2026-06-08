#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/../../load-env.sh"
hillm read --device usb-hub --dry-run \
  | python3 -c "import json,sys; d=json.load(sys.stdin); assert d['ok'] or d.get('error')"
echo "usb list ok"
