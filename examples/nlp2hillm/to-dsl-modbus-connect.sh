#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/../load-env.sh"
line="$(nlp2hillm 'connect modbus device' --no-llm)"
[[ "$line" == "CONNECT DEVICE modbus-rtu" ]]
echo "to-dsl modbus connect ok: $line"
