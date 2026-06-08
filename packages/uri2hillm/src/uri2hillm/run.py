from __future__ import annotations

from dsl2hillm import dispatch
from hillm.project_env import apply_execution_policy
from uri2hillm.decode import uri_to_dsl


def run_uri(
    uri: str,
    *,
    default_file: str | None = None,
    live: bool = False,
    dry_run: bool = False,
):
    line = uri_to_dsl(uri, default_file=default_file)
    line = apply_execution_policy(line, live=live, dry_run=dry_run, respect_env=not live)
    return dispatch(line, default_file=default_file)
