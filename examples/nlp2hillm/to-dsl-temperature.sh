#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/../load-env.sh"
line="$(nlp2hillm 'read temperature from serial' --no-llm)"
[[ "$line" == "READ DEVICE sensor-temp REGISTER temperature" ]]
echo "to-dsl temperature ok: $line"
