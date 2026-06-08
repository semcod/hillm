#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/../load-env.sh"
cli2hillm HEALTH | python3 -c "import json,sys; d=json.load(sys.stdin); assert d['ok']"
cli2hillm 'devices --format json' --shell | python3 -c "import json,sys; d=json.load(sys.stdin); assert len(d)>=10"
echo "cli2hillm ok"
