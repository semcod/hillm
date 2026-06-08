#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/../load-env.sh"
line="$(nlp2hillm 'what port is the mouse on' --no-llm)"
[[ "$line" == "STATUS DEVICE mouse-default" ]]
echo "to-dsl mouse status (en) ok: $line"
