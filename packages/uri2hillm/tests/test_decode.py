from __future__ import annotations

import pytest

from uri2hillm.decode import uri_to_dsl
from uri2hillm.uri import dsl_line_to_uri, normalize_uri_input, uri_for_cmd


def test_normalize_uri_input_accepts_full_uri() -> None:
    uri = uri_for_cmd("READ", device="camera-usb", dry_run=True)
    assert normalize_uri_input(uri) == uri


def test_normalize_uri_input_accepts_dsl_shorthand() -> None:
    uri = normalize_uri_input("READ DEVICE sensor-temp DRY_RUN true")
    assert uri == uri_for_cmd("READ", device="sensor-temp", dry_run=True)


def test_normalize_uri_input_accepts_bare_verb() -> None:
    assert normalize_uri_input("HEALTH") == uri_for_cmd("HEALTH")
    assert normalize_uri_input("READ") == uri_for_cmd("READ")


def test_dsl_line_to_uri_round_trip() -> None:
    uri = dsl_line_to_uri("READ DEVICE camera-usb DRY_RUN true")
    assert uri_to_dsl(uri) == "READ DEVICE camera-usb DRY_RUN true"


def test_uri_to_dsl_bare_input_hint() -> None:
    with pytest.raises(ValueError, match="expected hillm:// URI or DSL line"):
        uri_to_dsl("READ")
