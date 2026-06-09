#!/usr/bin/env bash
# Show auto-fallback serial address for sensor-temp (ttyACM0 when ttyUSB0 missing).
set -euo pipefail
source "$(dirname "$0")/../../load-env.sh"
python3 -c "
from hillm.registry import get_device_spec, first_existing_serial_path
spec = get_device_spec('sensor-temp')
addr = spec.resolve_address()
print('resolved:', addr)
if addr.startswith('/dev/'):
    import os
    print('exists:', os.path.exists(addr))
print('first serial:', first_existing_serial_path('/dev/ttyUSB0', '/dev/ttyACM0') or '(none)')
"
echo "sensor resolve address ok"
