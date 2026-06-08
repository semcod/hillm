#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/../load-env.sh"
line="$(nlp2hillm 'capture image from camera' --no-llm)"
[[ "$line" == "ACTUATE DEVICE camera-usb ACTION capture" ]]
echo "to-dsl camera ok: $line"
