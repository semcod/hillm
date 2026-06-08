from __future__ import annotations

import pytest

from uri2hillm.compile import compile_hillm_uri
from uri2hillm.uri import is_hillm_uri, uri_for_cmd

nlp2uri = pytest.importorskip("nlp2uri.models")


def test_uri_for_cmd_builds_query() -> None:
    uri = uri_for_cmd("READ", device="camera-usb", dry_run=True)
    assert is_hillm_uri(uri)
    assert "device=camera-usb" in uri


def test_compile_hillm_uri_os_action() -> None:
    from nlp2uri.models import HostPlatform

    uri = uri_for_cmd("HEALTH")
    actions = compile_hillm_uri(uri, HostPlatform.LINUX)
    assert actions[0].args == [uri]
