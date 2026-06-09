#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/../load-env.sh"
line="$(uri2hillm decode 'hillm://cmd/READ?device=sensor-temp&dry_run=true')"
[[ "$line" == "READ DEVICE sensor-temp DRY_RUN true" ]]
echo "uri decode sensor ok: $line"
