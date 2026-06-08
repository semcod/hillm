#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/../load-env.sh"
line="$(nlp2hillm 'read temperature from serial')"
[[ "$line" == *"READ"* ]]
nlp2hillm 'connect modbus device' --apply | python3 -c "import json,sys; d=json.load(sys.stdin); assert d['ok']"
echo "nlp ok"
