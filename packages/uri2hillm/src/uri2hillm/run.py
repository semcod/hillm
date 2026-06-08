from __future__ import annotations

from dsl2hillm import dispatch
from uri2hillm.decode import uri_to_dsl


def run_uri(uri: str, *, default_file: str | None = None):
    line = uri_to_dsl(uri, default_file=default_file)
    return dispatch(line, default_file=default_file)
