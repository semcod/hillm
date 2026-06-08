from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from dsl2hillm.bus import dispatch
from dsl2hillm.events import EventStore
from dsl2hillm.schema_registry import schema_for_verb, validate_schemas
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response

DEFAULT_PORT = 8218


def create_app() -> FastAPI:
    app = FastAPI(title="rest2hillm", version="0.1.0")

    @app.get("/")
    def root() -> dict[str, Any]:
        return {
            "service": "rest2hillm",
            "health": "/health",
            "dsl": "POST /v1/dsl",
            "schema": "GET /v1/schema/{verb}",
            "port": DEFAULT_PORT,
            "example": "curl -X POST http://127.0.0.1:8218/v1/dsl -d HEALTH",
        }

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/v1/schema/{verb}")
    def get_schema(verb: str) -> dict[str, Any]:
        return schema_for_verb(verb)

    @app.get("/v1/schema")
    def validate_all() -> dict[str, Any]:
        errors = validate_schemas()
        return {"ok": not errors, "errors": errors}

    @app.post("/v1/dsl")
    async def post_dsl(request: Request, file: str = "") -> Response:
        content_type = request.headers.get("content-type", "text/plain").split(";")[0].strip()
        body = await request.body()
        if content_type == "application/json":
            payload = json.loads(body.decode("utf-8"))
            result = dispatch(payload, default_file=file or None)
        else:
            line = body.decode("utf-8").strip()
            result = dispatch(line, default_file=file or None)
        return JSONResponse(result.to_dict())

    @app.get("/v1/events")
    def get_events(file: str = ".") -> JSONResponse:
        store = EventStore.for_workdir(Path(file))
        events = [event.to_dict() for event in store.read_all()]
        return JSONResponse(events)

    return app
