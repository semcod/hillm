#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/../load-env.sh"

out="$(nlp2hillm 'read temperature from serial' --no-llm -v 2>&1)"
echo "$out" | grep -q '# mapped via: rules'
echo "$out" | grep -q 'READ DEVICE sensor-temp REGISTER temperature'
echo "nlp2hillm verbose rules ok"
