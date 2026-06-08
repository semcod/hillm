#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/../load-env.sh"
line="$(nlp2hillm 'jakie urządzenia usb są podłączone' --no-llm)"
[[ "$line" == "DEVICES CATEGORY usb" ]]
echo "to-dsl list usb ok: $line"
