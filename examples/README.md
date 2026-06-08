# hillm examples — hardware smoke tests

Runnable scripts to exercise HILLM through CLI, DSL, and control-layer adapters.
All examples default to **dry-run** via `HILLM_DRY_RUN=1`.

## Quick start

```bash
cd /home/tom/github/semcod/hillm
bash packages/install-dev.sh
cp examples/env.example .env   # optional

bash examples/cli/devices.sh
bash examples/dsl/run-smoke.sh
bash examples/run-all-dry-run.sh
```

## Layout

| Path | Focus |
|------|-------|
| [cli/](cli/) | `hillm` CLI — devices, scan, read, write, actuate |
| [dsl/](dsl/) | `dsl2hillm` query/command smoke |
| [control-layer/](control-layer/) | `uri2hillm`, `nlp2hillm`, `cli2hillm`, `rest2hillm` |
| [devices/](devices/) | Per-category hardware profiles |
| [nlp2uri/](nlp2uri/) | `nlp2uri` compile + `uri2hillm` dispatch |

## Device categories

| Category | Example device id | Script |
|----------|-------------------|--------|
| display / HDMI | `display-primary` | [devices/display/status.sh](devices/display/status.sh) |
| camera | `camera-usb` | [devices/camera/capture-dry-run.sh](devices/camera/capture-dry-run.sh) |
| audio | `speaker-default` | [devices/audio/status.sh](devices/audio/status.sh) |
| USB | `usb-hub` | [devices/usb/list.sh](devices/usb/list.sh) |
| serial / RS232 | `serial-ttyacm0` | [devices/serial/read-dry-run.sh](devices/serial/read-dry-run.sh) |
| Modbus | `modbus-tcp` | [devices/modbus/read-dry-run.sh](devices/modbus/read-dry-run.sh) |

## REST note

`control-layer/rest-health.sh` requires a running `rest2hillm` server. The aggregate
`run-all-dry-run.sh` skips it when the server is offline.

## See also

- [docs/README.md](../docs/README.md) — documentation index
- [docs/configuration.md](../docs/configuration.md)
- [docs/control-layer.md](../docs/control-layer.md)
- [packages/README.md](../packages/README.md)
- [CHANGELOG.md](../CHANGELOG.md)
- [TODO.md](../TODO.md)
