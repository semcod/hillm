#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/../load-env.sh"

nlp2hillm 'na jakim porcie jest podłączona myszka?' --no-llm --apply \
  | python3 -c "
import json, sys
d = json.load(sys.stdin)
assert d['ok'], d.get('error', d)
assert d['command'] == 'STATUS DEVICE mouse-default DRY_RUN true'
assert d['data']['device_id'] == 'mouse-default'
assert d['data']['backend'] == 'dry_run'
"

echo "nlp2hillm status mouse dry-run ok"
