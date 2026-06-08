#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/../load-env.sh"

port="${REST2HILLM_PORT:-8218}"
base="http://127.0.0.1:${port}"

if ! curl -sf "$base/health" >/dev/null 2>&1; then
  echo "error: rest2hillm not running on $base — start: rest2hillm --port $port" >&2
  exit 1
fi

curl -sf "$base/health" | python3 -m json.tool
curl -sf -X POST "$base/v1/dsl" -d HEALTH | python3 -m json.tool
echo "rest ok"
