from __future__ import annotations

from urllib.parse import parse_qs, urlparse


def uri_to_dsl(uri: str, *, default_file: str | None = None) -> str:
    del default_file
    parsed = urlparse(uri)
    if parsed.scheme != "hillm":
        if not parsed.scheme:
            raise ValueError(
                f"expected hillm:// URI or DSL line, got {uri!r}. "
                "Examples: uri2hillm HEALTH, "
                "uri2hillm 'hillm://cmd/READ?device=sensor-temp&dry_run=true', "
                "uri2hillm READ DEVICE sensor-temp DRY_RUN true"
            )
        raise ValueError(f"unsupported URI scheme: {parsed.scheme}")
    path = parsed.path.strip("/")
    verb = (path.split("/", 1)[0] if path else "HEALTH").upper()
    query = {k: v[-1] for k, v in parse_qs(parsed.query).items()}
    parts = [verb]
    for key in ("device", "register", "address", "value", "action", "category", "prompt"):
        if key in query and query[key]:
            parts.extend([key.upper(), query[key]])
    if query.get("dry_run", "").lower() in {"1", "true", "yes", "on"}:
        parts.extend(["DRY_RUN", "true"])
    return " ".join(parts)
