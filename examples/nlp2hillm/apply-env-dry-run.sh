#!/usr/bin/env bash
# HILLM_DRY_RUN=1 (from load-env.sh) auto-appends DRY_RUN on --apply
set -euo pipefail
source "$(dirname "$0")/../load-env.sh"

nlp2hillm 'read temperature from serial' --no-llm --apply \
  | python3 -c "
import json, sys
d = json.load(sys.stdin)
assert d['ok'], d.get('error', d)
assert 'DRY_RUN true' in d['command']
assert d['data']['backend'] == 'dry_run'
"

echo "nlp2hillm env dry-run ok"
