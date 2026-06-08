# rest2hillm

REST API (FastAPI) — `POST /v1/dsl`, port **8218**.

```bash
rest2hillm --port 8218
curl -sf http://127.0.0.1:8218/health
curl -sf -X POST http://127.0.0.1:8218/v1/dsl -d HEALTH
curl -sf -X POST http://127.0.0.1:8218/v1/dsl -d 'READ DEVICE sensor-temp DRY_RUN true'
```

Endpoints: `/health`, `/v1/dsl`, `/v1/schema/{verb}`, `/v1/events`.

**See also:** [examples/control-layer/rest-health.sh](../../examples/control-layer/rest-health.sh)
