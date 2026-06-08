"""hillm:// URI helpers for nlp2uri integration."""

from __future__ import annotations

from urllib.parse import quote, urlencode, urlparse

HILLM_SCHEME = "hillm"


def is_hillm_uri(uri: str) -> bool:
    try:
        return urlparse(uri).scheme.lower() == HILLM_SCHEME
    except Exception:
        return False


def uri_for_cmd(
    verb: str,
    *,
    device: str = "",
    register: str = "",
    address: str = "",
    value: str = "",
    action: str = "",
    category: str = "",
    prompt: str = "",
    dry_run: bool = False,
) -> str:
    """Build a hillm://cmd/{verb}?... URI."""
    params: dict[str, str] = {}
    if device:
        params["device"] = device
    if register:
        params["register"] = register
    if address:
        params["address"] = address
    if value:
        params["value"] = value
    if action:
        params["action"] = action
    if category:
        params["category"] = category
    if prompt:
        params["prompt"] = prompt
    if dry_run:
        params["dry_run"] = "true"
    query = urlencode(params, quote_via=quote)
    suffix = f"?{query}" if query else ""
    return f"{HILLM_SCHEME}://cmd/{verb.upper()}{suffix}"


def dsl_line_to_uri(line: str, *, default_file: str | None = None) -> str:
    """Convert a hillm DSL line to a hillm:// URI."""
    from dsl2hillm.grammar import parse_line

    payload = parse_line(line, default_file=default_file)
    if not payload:
        raise ValueError("empty command")
    value = payload.get("value")
    return uri_for_cmd(
        payload["verb"],
        device=payload.get("device", ""),
        register=payload.get("register", ""),
        address=payload.get("address", ""),
        value="" if value is None else str(value),
        action=payload.get("action", ""),
        category=payload.get("category", ""),
        prompt=payload.get("prompt", ""),
        dry_run=bool(payload.get("dry_run", False)),
    )


def normalize_uri_input(raw: str, *, default_file: str | None = None) -> str:
    """Accept a hillm:// URI or DSL shorthand (e.g. READ DEVICE sensor-temp)."""
    text = " ".join(raw.split())
    if not text:
        raise ValueError("empty command")
    if is_hillm_uri(text):
        return text
    if "://" in text:
        raise ValueError(
            f"unsupported URI in {text!r}; expected hillm://cmd/VERB?..."
        )
    return dsl_line_to_uri(text, default_file=default_file)
