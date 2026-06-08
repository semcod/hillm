#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/../load-env.sh"
uri='hillm://cmd/READ?device=sensor-temp&dry_run=true'
python3 - <<'PY'
from nlp2uri.compile import compile_uri_to_actions
from nlp2uri.models import HostPlatform

uri = "hillm://cmd/READ?device=sensor-temp&dry_run=true"
actions = compile_uri_to_actions(uri, HostPlatform.LINUX)
assert actions[0].command.endswith("uri2hillm")
assert actions[0].args[0] == uri
print("nlp2uri compile ok")
PY
