#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/../load-env.sh"
bash "$(dirname "$0")/../nlp2hillm/to-dsl-temperature.sh"
bash "$(dirname "$0")/../nlp2hillm/apply-connect-modbus.sh"
echo "nlp control-layer ok"
