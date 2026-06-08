#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/../load-env.sh"
python3 - <<'PY'
import json
from uri2hillm.run import run_uri
from uri2hillm.uri import uri_for_cmd

uri = uri_for_cmd("READ", device="sensor-temp", dry_run=True)
result = run_uri(uri)
assert result.ok, result.error
payload = json.loads(result.output)
assert payload["device_id"] == "sensor-temp"
print("nlp2uri run ok")
PY
