#!/usr/bin/env bash
# Optional: requires OPENROUTER_API_KEY in .env and nlp2hillm[llm]
set -euo pipefail
source "$(dirname "$0")/../load-env.sh"
if [[ -z "${OPENROUTER_API_KEY:-}" ]]; then
  echo "skip: OPENROUTER_API_KEY not set" >&2
  exit 0
fi
line="$(nlp2hillm 'read temperature from serial' --use-llm)"
[[ "$line" == *"READ"* ]]
[[ "$line" == *"sensor-temp"* ]] || [[ "$line" == *"DEVICE"* ]]
echo "nlp2hillm llm ok: $line"
