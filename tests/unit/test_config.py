import pytest

from tests.config import AutomationSettings


def test_default_settings_are_valid(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("VAIPEX_BASE_URL", raising=False)
    monkeypatch.delenv("VAIPEX_EXPECT_TIMEOUT_MS", raising=False)

    settings = AutomationSettings.from_environment("http://127.0.0.1:8000/")

    assert settings.base_url == "http://127.0.0.1:8000"
    assert settings.timeout_ms == 5000
    assert settings.user.email == "demo@vaipex.io"
    assert settings.shipping_address.city == "Cloud City"


def test_environment_overrides_are_applied(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("VAIPEX_BASE_URL", "https://store.example.test/")
    monkeypatch.setenv("VAIPEX_EXPECT_TIMEOUT_MS", "9000")
    monkeypatch.setenv("VAIPEX_DEMO_EMAIL", "automation@example.test")
    monkeypatch.setenv("VAIPEX_SHIPPING_CITY", "Test City")

    settings = AutomationSettings.from_environment("http://127.0.0.1:8000")

    assert settings.base_url == "https://store.example.test"
    assert settings.timeout_ms == 9000
    assert settings.user.email == "automation@example.test"
    assert settings.shipping_address.city == "Test City"


@pytest.mark.parametrize(
    ("name", "value", "message"),
    [
        ("VAIPEX_BASE_URL", "not-a-url", "absolute HTTP or HTTPS URL"),
        ("VAIPEX_EXPECT_TIMEOUT_MS", "slow", "must be an integer"),
        ("VAIPEX_EXPECT_TIMEOUT_MS", "0", "must be greater than zero"),
    ],
)
def test_invalid_settings_fail_fast(
    monkeypatch: pytest.MonkeyPatch,
    name: str,
    value: str,
    message: str,
) -> None:
    monkeypatch.setenv(name, value)

    with pytest.raises(ValueError, match=message):
        AutomationSettings.from_environment("http://127.0.0.1:8000")
