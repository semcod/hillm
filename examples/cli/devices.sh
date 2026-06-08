#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/../load-env.sh"
hillm devices --format json | python3 -c "import json,sys; d=json.load(sys.stdin); assert len(d)>=10"
echo "devices ok"
