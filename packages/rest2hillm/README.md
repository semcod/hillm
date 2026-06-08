# rest2hillm

REST API (FastAPI) — `POST /v1/dsl`, port **8218**.

`dispatch()` auto-loads `.env`; include `DRY_RUN true` in the DSL body for safe device commands.

```bash
rest2hillm --port 8218
curl -sf http://127.0.0.1:8218/health
curl -sf -X POST http://127.0.0.1:8218/v1/dsl -d HEALTH
curl -sf -X POST http://127.0.0.1:8218/v1/dsl -d 'READ DEVICE sensor-temp DRY_RUN true'
```

Endpoints: `/health`, `/v1/dsl`, `/v1/schema/{verb}`, `/v1/events`.

Pair with `rest2gillm` (:8220) and `rest2tillm` (:8216).

**See also:** [examples/control-layer/rest-health.sh](../../examples/control-layer/rest-health.sh) · [docs/configuration.md](../../docs/configuration.md)
