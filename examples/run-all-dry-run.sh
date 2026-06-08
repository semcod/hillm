#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")" && pwd)"
# shellcheck disable=SC1091
source "$root/load-env.sh"

run() {
  local script="$1"
  echo "=== $script ===" >&2
  if bash "$script" >/dev/null; then
    echo "ok: $script" >&2
  else
    echo "fail: $script" >&2
    return 1
  fi
}

scripts=(
  "$root/cli/devices.sh"
  "$root/cli/scan.sh"
  "$root/cli/read-dry-run.sh"
  "$root/cli/write-dry-run.sh"
  "$root/dsl/run-smoke.sh"
  "$root/control-layer/uri-dispatch.sh"
  "$root/control-layer/nlp-to-dsl.sh"
  "$root/nlp2hillm/to-dsl-temperature.sh"
  "$root/nlp2hillm/to-dsl-mouse.sh"
  "$root/nlp2hillm/to-dsl-mouse-port-pl.sh"
  "$root/nlp2hillm/to-dsl-mouse-status-en.sh"
  "$root/nlp2hillm/to-dsl-camera.sh"
  "$root/nlp2hillm/to-dsl-modbus-connect.sh"
  "$root/nlp2hillm/to-dsl-list-usb.sh"
  "$root/nlp2hillm/to-dsl-health.sh"
  "$root/nlp2hillm/apply-read-dry-run.sh"
  "$root/nlp2hillm/apply-env-dry-run.sh"
  "$root/nlp2hillm/apply-connect-modbus.sh"
  "$root/nlp2hillm/apply-status-mouse-dry-run.sh"
  "$root/nlp2hillm/apply-status-mouse-live.sh"
  "$root/nlp2hillm/apply-verbose-rules.sh"
  "$root/nlp2hillm/apply-temperature-live.sh"
  "$root/control-layer/cli-exec.sh"
  "$root/devices/display/status.sh"
  "$root/devices/camera/capture-dry-run.sh"
  "$root/devices/audio/status.sh"
  "$root/devices/usb/list.sh"
  "$root/devices/serial/read-dry-run.sh"
  "$root/devices/modbus/read-dry-run.sh"
)

if python3 -c "import nlp2uri, uri2hillm" 2>/dev/null; then
  scripts+=("$root/nlp2uri/compile-uri.sh" "$root/nlp2uri/run-uri.sh")
fi

for script in "${scripts[@]}"; do
  run "$script"
done

if bash "$root/control-layer/rest-health.sh" >/dev/null 2>&1; then
  echo "ok: rest-health (server was up)" >&2
else
  echo "skip: rest-health (start rest2hillm --port 8218 to test)" >&2
fi

echo "done" >&2
