#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/../load-env.sh"
uri2hillm 'hillm://cmd/HEALTH' | python3 -c "import json,sys; d=json.load(sys.stdin); assert d['ok'] and d['verb']=='HEALTH'"
uri2hillm 'hillm://cmd/READ?device=sensor-temp&dry_run=true' \
  | python3 -c "import json,sys; d=json.load(sys.stdin); assert d['ok']"
echo "uri dispatch ok"
