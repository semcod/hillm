from dsl2hillm import dispatch


def test_health_query() -> None:
    result = dispatch("HEALTH")
    assert result.ok
    assert result.verb == "HEALTH"


def test_devices_query() -> None:
    result = dispatch("DEVICES CATEGORY serial")
    assert result.ok
    assert "devices" in result.data


def test_validate_without_device() -> None:
    result = dispatch("VALIDATE")
    assert result.ok
    assert result.data.get("package") == "hillm"
