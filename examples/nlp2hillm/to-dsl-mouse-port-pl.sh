#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/../load-env.sh"
line="$(nlp2hillm 'na jakim porcie jest podłączona myszka?' --no-llm)"
[[ "$line" == "STATUS DEVICE mouse-default" ]]
echo "to-dsl mouse port (pl) ok: $line"
