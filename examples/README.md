# hillm examples — hardware smoke tests

Runnable scripts to exercise HILLM through CLI, DSL, NLP, and control-layer adapters.
Scripts source [load-env.sh](load-env.sh) which sets `HILLM_DRY_RUN=1` by default.

## Quick start

```bash
cd /home/tom/github/semcod/hillm
bash packages/install-dev.sh
cp examples/env.example .env   # append HILLM_DRY_RUN=1 if .env already exists

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
| [nlp2hillm/](nlp2hillm/) | NL → DSL mapping and `--apply` (dry-run default) |
| [devices/](devices/) | Per-category hardware profiles |
| [nlp2uri/](nlp2uri/) | `nlp2uri` compile + `uri2hillm` dispatch |

## nlp2hillm

Natural language → DSL mapping and optional execution. Scripts use `--no-llm` for deterministic CI; live scripts skip gracefully when hardware or `pyserial` is missing.

### Mapping only (`to-dsl-*.sh`)

| Script | Prompt | Expected DSL |
|--------|--------|--------------|
| [to-dsl-temperature.sh](nlp2hillm/to-dsl-temperature.sh) | `read temperature from serial` | `READ DEVICE sensor-temp REGISTER temperature` |
| [to-dsl-mouse.sh](nlp2hillm/to-dsl-mouse.sh) | `read usb port for mouse` | `READ DEVICE mouse-default` |
| [to-dsl-mouse-port-pl.sh](nlp2hillm/to-dsl-mouse-port-pl.sh) | `na jakim porcie jest podłączona myszka?` | `STATUS DEVICE mouse-default` |
| [to-dsl-mouse-status-en.sh](nlp2hillm/to-dsl-mouse-status-en.sh) | `what port is the mouse on` | `STATUS DEVICE mouse-default` |
| [to-dsl-camera.sh](nlp2hillm/to-dsl-camera.sh) | `capture image from camera` | `ACTUATE DEVICE camera-usb ACTION capture` |
| [to-dsl-modbus-connect.sh](nlp2hillm/to-dsl-modbus-connect.sh) | `connect modbus device` | `CONNECT DEVICE modbus-rtu` |
| [to-dsl-list-usb.sh](nlp2hillm/to-dsl-list-usb.sh) | `jakie urządzenia usb są podłączone` | `DEVICES CATEGORY usb` |
| [to-dsl-health.sh](nlp2hillm/to-dsl-health.sh) | `HEALTH` | `HEALTH` |

### Execution (`apply-*.sh`)

| Script | What it tests |
|--------|---------------|
| [apply-read-dry-run.sh](nlp2hillm/apply-read-dry-run.sh) | `--apply` default dry-run for READ |
| [apply-env-dry-run.sh](nlp2hillm/apply-env-dry-run.sh) | `HILLM_DRY_RUN=1` from load-env |
| [apply-connect-modbus.sh](nlp2hillm/apply-connect-modbus.sh) | `connect modbus device --apply` |
| [apply-status-mouse-dry-run.sh](nlp2hillm/apply-status-mouse-dry-run.sh) | Polish mouse port question → dry-run STATUS |
| [apply-status-mouse-live.sh](nlp2hillm/apply-status-mouse-live.sh) | Live mouse scan under `/dev/input/by-id` (skip if missing) |
| [apply-verbose-rules.sh](nlp2hillm/apply-verbose-rules.sh) | `-v` prints `# mapped via: rules` |
| [apply-temperature-live.sh](nlp2hillm/apply-temperature-live.sh) | Live serial read (skip without port/pyserial) |
| [llm-openrouter.sh](nlp2hillm/llm-openrouter.sh) | Optional LLM mapping (skip without API key) |

```bash
# Quick smoke
bash examples/nlp2hillm/to-dsl-temperature.sh
bash examples/nlp2hillm/to-dsl-mouse-port-pl.sh
bash examples/nlp2hillm/apply-read-dry-run.sh
bash examples/nlp2hillm/apply-status-mouse-live.sh

# All nlp2hillm examples
for s in examples/nlp2hillm/*.sh; do bash "$s"; done
```

`nlp2hillm --apply` uses dry-run by default; pass `--live` for real hardware. Live scripts call `unset HILLM_DRY_RUN` because [load-env.sh](load-env.sh) sets `HILLM_DRY_RUN=1`.

Full mapping table and troubleshooting: [packages/nlp2hillm/README.md](../packages/nlp2hillm/README.md).

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
