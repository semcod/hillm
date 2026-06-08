"""Compile hillm:// to OS actions (nlp2uri integration)."""

from __future__ import annotations

import shutil
from typing import Any

from uri2hillm.uri import is_hillm_uri


def compile_hillm_uri(uri: str, host: Any) -> list[Any]:
    """Return OSAction list that invokes uri2hillm with the URI."""
    if not is_hillm_uri(uri):
        raise ValueError(f"not a hillm uri: {uri}")

    try:
        from nlp2uri.models import OSAction
    except ImportError as exc:
        raise RuntimeError("compile_hillm_uri requires nlp2uri") from exc

    runner = shutil.which("uri2hillm") or "uri2hillm"
    return [OSAction(host, runner, [uri])]
