#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/../../load-env.sh"
hillm status --device speaker-default --dry-run \
  | python3 -c "import json,sys; d=json.load(sys.stdin); assert d['device_id']=='speaker-default'"
echo "audio status ok"
