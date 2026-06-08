#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/../../load-env.sh"
hillm read --device serial-ttyacm0 --dry-run \
  | python3 -c "import json,sys; d=json.load(sys.stdin); assert d['ok']"
echo "serial read dry-run ok"
