#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/../../load-env.sh"
hillm actuate --device camera-usb --action capture --dry-run \
  | python3 -c "import json,sys; d=json.load(sys.stdin); assert d['ok']"
echo "camera capture dry-run ok"
