from __future__ import annotations

from unittest.mock import patch

from nlp2hillm.llm_backend import LLMBackend, nl_to_dsl_line


class _FakeBackend:
    def complete(self, *, model, messages, temperature=0.2, response_format=None) -> str:
        return '{"dsl": "READ DEVICE sensor-temp REGISTER temperature"}'


def test_nl_to_dsl_line_fake_backend() -> None:
    with patch.dict("os.environ", {"OPENROUTER_API_KEY": "sk-test"}, clear=False):
        line = nl_to_dsl_line("read temperature from serial", backend=_FakeBackend())
    assert line == "READ DEVICE sensor-temp REGISTER temperature"


def test_nl_to_dsl_line_without_api_key() -> None:
    with patch.dict("os.environ", {}, clear=True):
        assert nl_to_dsl_line("read temperature") is None
