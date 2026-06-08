#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/../load-env.sh"
line="$(nlp2hillm 'read usb port for mouse' --no-llm)"
[[ "$line" == "READ DEVICE mouse-default" ]]
echo "to-dsl mouse ok: $line"
