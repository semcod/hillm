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
make test-examples             # pytest wrapper for all CORE_SCRIPTS
```

## Layout

| Path | Focus |
|------|-------|
| [cli/](cli/) | `hillm` CLI — devices, scan, read, write, status |
| [dsl/](dsl/) | `dsl2hillm` query/command smoke |
| [control-layer/](control-layer/) | `uri2hillm`, `nlp2hillm`, `cli2hillm`, `rest2hillm` |
| [nlp2hillm/](nlp2hillm/) | NL → DSL mapping and `--apply` (dry-run default) |
| [devices/](devices/) | Per-category hardware profiles |
| [nlp2uri/](nlp2uri/) | `nlp2uri` compile + `uri2hillm` dispatch |

## cli/

| Script | What it tests |
|--------|---------------|
| [devices.sh](cli/devices.sh) | `hillm devices` |
| [scan.sh](cli/scan.sh) | `hillm scan` |
| [read-dry-run.sh](cli/read-dry-run.sh) | `hillm read --device sensor-temp --dry-run` |
| [write-dry-run.sh](cli/write-dry-run.sh) | `hillm write` dry-run |
| [status-ecosystem.sh](cli/status-ecosystem.sh) | `hillm status --ecosystem` |
| [status-mouse-dry-run.sh](cli/status-mouse-dry-run.sh) | `hillm status --device mouse-default --dry-run` |
| [dsl-health.sh](cli/dsl-health.sh) | `dsl2hillm HEALTH` via CLI path |

## dsl/

| Script | What it tests |
|--------|---------------|
| [run-smoke.sh](dsl/run-smoke.sh) | Multi-line [smoke.dsl](dsl/smoke.dsl) |
| [read-sensor-temp.sh](dsl/read-sensor-temp.sh) | `READ DEVICE sensor-temp` dry-run |
| [devices-usb.sh](dsl/devices-usb.sh) | `DEVICES CATEGORY usb` |

## control-layer/

| Script | What it tests |
|--------|---------------|
| [uri-dispatch.sh](control-layer/uri-dispatch.sh) | `uri2hillm` HEALTH + READ URI |
| [uri-shorthand-read.sh](control-layer/uri-shorthand-read.sh) | DSL shorthand `READ DEVICE sensor-temp` |
| [uri-decode-sensor.sh](control-layer/uri-decode-sensor.sh) | `uri2hillm decode hillm://…` → DSL |
| [nlp-to-dsl.sh](control-layer/nlp-to-dsl.sh) | NL temperature + modbus connect |
| [nlp-mouse-port.sh](control-layer/nlp-mouse-port.sh) | PL mouse port → STATUS dry-run |
| [dsl-live-policy.sh](control-layer/dsl-live-policy.sh) | `dsl2hillm` dry-run default vs `--live` |
| [cli-exec.sh](control-layer/cli-exec.sh) | `cli2hillm` passthrough |
| [rest-health.sh](control-layer/rest-health.sh) | REST server (optional, skip if offline) |

## nlp2hillm/

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
| [apply-status-mouse-dry-run.sh](nlp2hillm/apply-status-mouse-dry-run.sh) | Polish mouse port → dry-run STATUS |
| [apply-status-mouse-live.sh](nlp2hillm/apply-status-mouse-live.sh) | Live mouse under `/dev/input/by-id` |
| [apply-verbose-rules.sh](nlp2hillm/apply-verbose-rules.sh) | `-v` → `# mapped via: rules` |
| [apply-temperature-live.sh](nlp2hillm/apply-temperature-live.sh) | Live serial read (skip without port/pyserial) |
| [check-serial-env.sh](nlp2hillm/check-serial-env.sh) | Install + port resolution diagnostics |
| [llm-openrouter.sh](nlp2hillm/llm-openrouter.sh) | Optional LLM (skip without API key) |

## devices/

| Category | Device id | Script |
|----------|-----------|--------|
| display / HDMI | `display-primary` | [display/status.sh](devices/display/status.sh) |
| camera | `camera-usb` | [camera/capture-dry-run.sh](devices/camera/capture-dry-run.sh) |
| audio | `speaker-default` | [audio/status.sh](devices/audio/status.sh) |
| USB | `usb-hub` | [usb/list.sh](devices/usb/list.sh) |
| serial | `serial-ttyacm0` | [serial/read-dry-run.sh](devices/serial/read-dry-run.sh) |
| Modbus | `modbus-tcp` | [modbus/read-dry-run.sh](devices/modbus/read-dry-run.sh) |
| input / mouse | `mouse-default` | [input/mouse-status-live.sh](devices/input/mouse-status-live.sh) |
| sensor / temp | `sensor-temp` | [sensor/temp-read-dry-run.sh](devices/sensor/temp-read-dry-run.sh) |
| sensor / temp | `sensor-temp` | [sensor/temp-status-live.sh](devices/sensor/temp-status-live.sh) |
| sensor / temp | `sensor-temp` | [sensor/temp-resolve-address.sh](devices/sensor/temp-resolve-address.sh) |

## nlp2uri/

| Script | What it tests |
|--------|---------------|
| [compile-uri.sh](nlp2uri/compile-uri.sh) | `nlp2uri` compile |
| [run-uri.sh](nlp2uri/run-uri.sh) | `uri2hillm` dispatch |

Requires `pip install nlp2uri[hillm]` (optional in CI).

## Run all

```bash
bash examples/run-all-dry-run.sh
make test-examples
```

`nlp2hillm --apply` uses dry-run by default; pass `--live` for real hardware. Live scripts call `unset HILLM_DRY_RUN` because [load-env.sh](load-env.sh) sets `HILLM_DRY_RUN=1`.

## See also

- [packages/nlp2hillm/README.md](../packages/nlp2hillm/README.md) — NL mapping table + troubleshooting
- [docs/README.md](../docs/README.md) — documentation index
- [docs/configuration.md](../docs/configuration.md)
- [docs/control-layer.md](../docs/control-layer.md)
- [CHANGELOG.md](../CHANGELOG.md)
- [TODO.md](../TODO.md)
