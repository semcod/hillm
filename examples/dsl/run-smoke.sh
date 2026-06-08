#!/usr/bin/env bash
set -euo pipefail
# shellcheck disable=SC1091
source "$(dirname "$0")/../load-env.sh"
script="$(dirname "$0")/smoke.dsl"

while IFS= read -r line || [[ -n "$line" ]]; do
  line="${line%%#*}"
  line="$(echo "$line" | xargs)"
  [[ -z "$line" ]] && continue
  if ! dsl2hillm "$line" >/dev/null; then
    echo "dsl failed: $line" >&2
    exit 1
  fi
done < "$script"

echo "dsl smoke ok"
