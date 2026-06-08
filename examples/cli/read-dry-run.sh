#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/../load-env.sh"
hillm read --device sensor-temp --dry-run | python3 -c "import json,sys; d=json.load(sys.stdin); assert d['ok']"
echo "read dry-run ok"
