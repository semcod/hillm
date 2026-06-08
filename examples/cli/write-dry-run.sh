#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/../load-env.sh"
hillm write --device actuator-relay --value 1 --register coil:0 --dry-run \
  | python3 -c "import json,sys; d=json.load(sys.stdin); assert d['ok']"
echo "write dry-run ok"
