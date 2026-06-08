#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/../load-env.sh"
line="$(nlp2hillm 'HEALTH' --no-llm)"
[[ "$line" == "HEALTH" ]]
echo "to-dsl health ok: $line"
