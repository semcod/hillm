# TODO

## High priority

- [x] Initial HILLM scaffold: registry, controller, transports, CLI
- [x] Control layer packages (`dsl2hillm`, `uri2hillm`, `nlp2hillm`, `cli2hillm`, `mcp2hillm`, `rest2hillm`)
- [x] nlp2uri integration via `hillm://` URIs (`nlp2uri[hillm]`)
- [x] `uri2hillm` DSL shorthand CLI (`HEALTH`, `READ DEVICE …`, `decode` / `run`)
- [ ] Publish `hillm` and `*2hillm` packages to PyPI

## Transports & devices

- [ ] Real GPIO backend (platform-specific)
- [ ] Live integration tests: serial, Modbus RTU/TCP, MQTT
- [ ] Per-category device docs under `docs/devices/`

## Control layer

- [ ] `rest2hillm` live server smoke in CI
- [ ] MCP tool coverage for all query verbs
- [ ] Optional: `uri2hillm` default device hint when `READ` omits `DEVICE`

## Docker / deploy

- [ ] Production-ready images (compose is currently a scaffold)
- [ ] Document hardware host requirements in `docs/configuration.md`

## Documentation

- [x] [docs/configuration.md](docs/configuration.md) — env vars, install profiles, ports
- [x] [docs/control-layer.md](docs/control-layer.md) — `*2hillm` overview
- [x] [docs/README.md](docs/README.md) — documentation index
- [x] [examples/README.md](examples/README.md) — runnable smoke scripts
- [x] [packages/README.md](packages/README.md) — control layer package matrix
- [ ] Per-device category docs: display, camera, audio, serial, Modbus, MQTT
- [ ] `SUMD.md` aligned with DSL verbs and device registry

## Testing

- [x] Core + control-layer pytest (34 tests)
- [x] [examples/run-all-dry-run.sh](examples/run-all-dry-run.sh) aggregate smoke
- [ ] `make lint` / ruff cleanup (style only, non-blocking)

**See also:** [CHANGELOG.md](CHANGELOG.md) · [README.md](README.md) · [docs/README.md](docs/README.md)
