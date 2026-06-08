# HILLM configuration

## Install profiles

```bash
pip install -e .                              # core only
pip install -e ".[serial,modbus,mqtt]"        # field transports
pip install -e ".[control]"                   # all *2hillm adapters
bash packages/install-dev.sh                  # editable control layer
```

## Environment variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `HILLM_DRY_RUN` | off | Force `dry_run` transport for every device |
| `HILLM_MODBUS_HOST` | — | Required for `modbus-tcp` profile readiness |
| `HILLM_MODBUS_PORT` | — | Required for `modbus-rtu` profile readiness |
| `HILLM_MQTT_URL` | — | Required for `mqtt-broker` profile readiness |
| `HILLM_<DEVICE_ID>_ADDRESS` | profile default | Per-device address override (`-` → `_`) |

Example:

```bash
export HILLM_DRY_RUN=1
export HILLM_SENSOR_TEMP_ADDRESS=/dev/ttyACM0
hillm read --device sensor-temp
```

## REST port

`rest2hillm` listens on **8218** by default (gillm uses 8220, tillm uses 8216).

## uri2hillm

`uri2hillm` accepts a full `hillm://` URI or DSL shorthand:

```bash
uri2hillm HEALTH
uri2hillm READ DEVICE sensor-temp DRY_RUN true
uri2hillm 'hillm://cmd/READ?device=camera-usb&dry_run=true'
uri2hillm decode READ DEVICE sensor-temp
uri2hillm run HEALTH
```

Bare `READ` without `DEVICE` returns a schema validation error (device is required).

Details: [control-layer.md](control-layer.md) · [packages/uri2hillm/README.md](../packages/uri2hillm/README.md)

## Koru / nlp2uri

- Koru compat: `hillm.compat` exports `hillm_shell` backend profile.
- nlp2uri: `hillm://` URIs compile to `uri2hillm <uri>` when `pip install nlp2uri[hillm]`.
- Examples: [examples/nlp2uri/](../examples/nlp2uri/)

## See also

- [README.md](README.md) — documentation index
- [control-layer.md](control-layer.md) — `*2hillm` adapters
- [examples/README.md](../examples/README.md)
- [packages/README.md](../packages/README.md)
- [CHANGELOG.md](../CHANGELOG.md)
- [TODO.md](../TODO.md)
