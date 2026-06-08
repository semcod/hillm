#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/../load-env.sh"
hillm scan | python3 -c "import json,sys; d=json.load(sys.stdin); assert 'platform' in d and 'devices' in d"
echo "scan ok"
